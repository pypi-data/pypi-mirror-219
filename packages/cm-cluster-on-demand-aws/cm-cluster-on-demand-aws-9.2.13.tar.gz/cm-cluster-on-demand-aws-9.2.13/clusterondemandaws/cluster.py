# Copyright 2004-2023 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import collections
import hashlib
import logging
from enum import Enum, auto
from functools import lru_cache

import tenacity

from clusterondemand.exceptions import CODException, UserReportableException
from clusterondemandaws.ec2connection import create_ec2_resource_client
from clusterondemandconfig import config

from . import efs
from .vpc import BCM_TYPE_HEAD_NODE

log = logging.getLogger("cluster-on-demand")


class Cluster(object):
    # AWS eIP assignment failures occur rarely and can be worked around
    # by retrying for 2.5+ minutes (see CM-9991).
    # Let's make it 5 minutes to make sure we don't leave an eIP allocation unassigned,
    # which costs money.
    IP_ASSIGNMENT_RETRY_DELAY = 10
    IP_ASSIGNMENT_RETRIES = 30

    def __init__(self, aws_session, name, head_node_image=None, vpc=None, primary_head_node=None,
                 secondary_head_node=None):
        self.efs_client = aws_session.client("efs")
        self.ec2, self.ec2c = create_ec2_resource_client(aws_session)
        self.name = name
        self.vpc = vpc
        self.head_node_image = head_node_image
        self.primary_head_node = primary_head_node
        self.secondary_head_node = secondary_head_node
        self.active_head_node = None
        self.passive_head_node = None
        self.is_ha = False  # To easily tell if the cluster is HA
        self.set_head_nodes()  # populates primary_head_node and secondary_head_node in case they weren't provided
        self.set_active_passive_head_nodes()
        self.error_message = None

    @classmethod
    def get_vpc_name(cls, vpc):
        for tag in vpc.tags:
            if tag["Key"] == "Name":
                return tag["Value"]

        raise CODException("No Name tag found")

    @classmethod
    def find(cls, aws_session, names):
        ec2, _ = create_ec2_resource_client(aws_session)
        patterns = [f"{config['fixed_cluster_prefix']}{name}" for name in names]
        log.debug("Searching for vpcs with tag:name %s" % patterns)
        for vpc in ec2.vpcs.filter(
                Filters=[{"Name": "tag:Name",
                          "Values": patterns}]):
            vpc_name = cls.get_vpc_name(vpc)
            cluster_name = vpc_name[len(config["fixed_cluster_prefix"]):]
            yield cls(aws_session, cluster_name, vpc=vpc)

    def __unicode__(self):
        return "{} {!r} {!r} {}".format(self.name,
                                        self.vpc,
                                        self.primary_head_node,
                                        self.primary_head_node and self.primary_head_node.state["Name"])

    def find_head_nodes(self):
        if not self.vpc:
            return None

        instances = list(self.vpc.instances.filter(Filters=[
            {"Name": "tag:BCM Type", "Values": [BCM_TYPE_HEAD_NODE]},
            {"Name": "instance-state-name",
             "Values": ["pending", "running", "shutting-down", "stopping", "stopped"]},
        ]))
        if not instances:
            return None

        return instances

    def set_head_nodes(self):
        head_nodes = self.find_head_nodes()
        if head_nodes and self.primary_head_node is None:
            if len(head_nodes) == 1:
                self.is_ha = False
                self.primary_head_node, self.secondary_head_node = head_nodes[0], None
            if len(head_nodes) == 2:
                self.is_ha = True
                first_hn_ha_tag = next((tag["Value"] for tag in head_nodes[0].tags if tag.get("Key") == "BCM HA"), None)
                if first_hn_ha_tag == "Secondary":
                    head_nodes.reverse()
                elif first_hn_ha_tag != "Primary":
                    log.warning(f"Expected tag 'BCM HA' not found for cluster {self.name}, "
                                f"primary headnode might be determined incorrectly")

                self.primary_head_node, self.secondary_head_node = head_nodes
            if len(head_nodes) > 2:
                raise CODException("More than two head nodes found for cluster %s (%r)" % (self.name, self.vpc))

    def set_active_passive_head_nodes(self):
        if not self.is_ha:
            return

        eip_and_associations = self.eip_and_associations
        if len(eip_and_associations.get(self.primary_head_node.id, [])) == 2:
            self.active_head_node = self.primary_head_node
            self.passive_head_node = self.secondary_head_node
        else:
            self.active_head_node = self.secondary_head_node
            self.passive_head_node = self.primary_head_node

    @property
    @lru_cache()
    def eip_and_associations(self):
        """
        Find network_interface.private_ip_addresses of both headnodes. Public EIP is associated with it,
        allowing to extract various useful data, such as public IP, AssociationId, AllocationId, etc. Those values
        can be used by other functions determine the active headnode, release EIP, etc.
        :return: {headnode instance id: [network_interface.private_ip_address]}
        """
        instance_addresses = {}  # maps instance_id to first network interface of the instance,
        # with private IP(s) of that interface nested within
        headnodes = self.find_head_nodes()
        for headnode in headnodes or []:
            headnode.reload()
            network_interface = headnode.network_interfaces[0]  # We only use the first interface
            network_interface.reload()
            instance_addresses[headnode.id] = network_interface.private_ip_addresses
        return instance_addresses

    class IpType(Enum):
        A = auto()
        B = auto()
        HA = auto()

    def tag_eip(self, ip_type, epialloc_id):
        if not epialloc_id:
            return

        tags = {
            "Name": {
                self.IpType.A: f"{self.name}-a public IP",
                self.IpType.B: f"{self.name}-b public IP",
                self.IpType.HA: f"{self.name} HA public IP",
            }[ip_type],
        }
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags
        self.ec2.create_tags(
            Resources=[epialloc_id],
            Tags=[{"Key": k, "Value": v} for k, v in tags.items()],
        )

    def assign_eips(self):
        eip_and_associations = self.eip_and_associations
        cluster_ips = []

        @tenacity.retry(
            wait=tenacity.wait_exponential(multiplier=1, max=self.IP_ASSIGNMENT_RETRY_DELAY),
            stop=tenacity.stop_after_attempt(self.IP_ASSIGNMENT_RETRIES),
            before_sleep=tenacity.before_sleep_log(log, logging.DEBUG),
            after=tenacity.after_log(log, logging.DEBUG),
            reraise=True,
        )
        def allocate_address(allocation_id, instance_id, private_ip):
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.associate_address
            self.ec2c.associate_address(
                AllocationId=allocation_id,
                InstanceId=instance_id,
                PrivateIpAddress=private_ip,
            )

        for instance_id, private_ip_addresses in eip_and_associations.items():
            for private_ip_address in private_ip_addresses:
                if not self.is_ha:
                    ip_type = self.IpType.A
                else:
                    if instance_id == self.primary_head_node.id and private_ip_address["Primary"]:
                        ip_type = self.IpType.A
                    elif instance_id == self.active_head_node.id and not private_ip_address["Primary"]:
                        ip_type = self.IpType.HA
                    elif instance_id == self.secondary_head_node.id and private_ip_address["Primary"]:
                        ip_type = self.IpType.B

                if private_ip_address.get("Association"):  # A public EIP is bound to the private_ip_address
                    allocation_ip = private_ip_address.get("Association")["PublicIp"]
                    cluster_ips.append((allocation_ip, ip_type.name))
                    continue  # If Elastic IP already assigned, don't allocate a new one

                # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.allocate_address
                allocation = self.ec2c.allocate_address(Domain="vpc")
                allocation_id = allocation["AllocationId"]
                allocation_ip = allocation["PublicIp"]
                private_ip = private_ip_address["PrivateIpAddress"]

                try:
                    allocate_address(allocation_id, instance_id, private_ip)
                except Exception as allocate_error:
                    try:
                        eip_assoc = private_ip_address["Association"]
                        self.ec2c.release_address(
                            AllocationId=eip_assoc["AllocationId"],
                        )
                    except Exception as release_error:
                        raise CODException("Error assigning IP", caused_by=release_error)
                    raise CODException("Error assigning IP", caused_by=allocate_error)

                self.tag_eip(ip_type=ip_type, epialloc_id=allocation_id)
                cluster_ips.append((allocation_ip, ip_type.name))
        if self.is_ha:
            cluster_ips.sort(key=lambda x: x[1])
            log.info(f"Cluster IPs: {', '.join([i[0] + ' ' + f'({i[1]})' for i in cluster_ips])}")
        else:
            log.info(f"Cluster IP: {cluster_ips[0][0]}")

    def release_eips(self):
        eip_and_associations = self.eip_and_associations
        for instance_id, private_ip_addresses in eip_and_associations.items():
            for private_ip_address in private_ip_addresses:
                if private_ip_address.get("Association"):  # A public EIP is bound to the private_ip_address
                    eip_assoc = private_ip_address.get("Association")
                    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.disassociate_address
                    self.ec2c.disassociate_address(
                        AssociationId=eip_assoc.get("AssociationId"),
                    )
                    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.release_address
                    self.ec2c.release_address(
                        AllocationId=eip_assoc.get("AllocationId"),
                    )
                    log.debug(f"Elastic IP {eip_assoc.get('PublicIp')} was released from instance {instance_id}")
                else:
                    log.debug(f"Private IP address {private_ip_address['PrivateIpAddress']} on {instance_id} has "
                              f"no Elastic IP associated, nothing to release")

    def get_efs_id(self):
        # The creation token is originally generated by cm-cloud-ha (see cluster-tools repo)
        # To be backward compatible, we check using both the old format and the new format
        old_efs_creation_token = f"bcm-ha-efs-{self.name}"
        efs_creation_token = hashlib.sha256(f"bcm-ha-efs-{self.name}".encode("utf-8")).hexdigest()

        response = efs.describe_fs(self.efs_client, token=efs_creation_token)
        if response:
            return response["FileSystemId"]
        elif len(old_efs_creation_token) <= 64:
            response = efs.describe_fs(self.efs_client, token=old_efs_creation_token)
            return response["FileSystemId"] if response else None
        else:
            return None

    def try_delete_efs(self):
        fs_id = self.get_efs_id()
        if not fs_id:
            return

        log.info(f"Deleting EFS {fs_id}...")
        response = efs.describe_mount_target(self.efs_client, fs_id=fs_id)
        if response:
            efs.delete_mount_target(self.efs_client, response["MountTargetId"])
        efs.delete_fs(self.efs_client, fs_id)

    @classmethod
    def destroy(cls, clusters):
        # Only destroy those for which vpc was actually created
        vpcs = [cluster.vpc for cluster in clusters if cluster.vpc]

        for cluster in clusters:
            cluster.release_eips()

        cls.terminate_instances_for_vpcs(vpcs)

        for cluster in clusters:
            cluster.try_delete_efs()

        cls.destroy_vpcs(vpcs)

        for cluster in clusters:
            cluster.vpc = None
            cluster.primary_head_node = None

    @classmethod
    def terminate_instances_for_vpcs(cls, vpcs):
        log.info("Stopping instances for VPCs %s", " ".join(cls.get_vpc_name(vpc) for vpc in vpcs))

        log.info("Listing instances...")
        instances = [
            instance
            for vpc in vpcs
            for instance in vpc.instances.all()
        ]

        # We want to terminate all instances here and wait until they are terminated.
        # That should be faster than
        # request termination and wait sequentially in destroy_vpc methods
        log.info(f"Issuing termination requests for {len(instances)} instances...")
        for instance in instances:
            instance.terminate()

        log.info("Waiting until instances terminated...")
        for instance in instances:
            instance.wait_until_terminated()

    @classmethod
    def destroy_vpcs(cls, vpcs):
        for vpc in vpcs:
            cls.destroy_vpc(vpc)

    @classmethod
    def destroy_vpc(cls, vpc):
        vpc_name = cls.get_vpc_name(vpc)
        log.info("Destroying VPC %s", vpc_name)

        log.info("Deleting subnets...")
        for subnet in vpc.subnets.all():
            subnet.delete()

        log.info("Deleting route tables...")
        for route_table in vpc.route_tables.all():
            if not cls._is_main_routing_table(route_table):
                route_table.delete()

        log.info("Detaching and deleting gateways...")
        for gateway in vpc.internet_gateways.all():
            vpc.detach_internet_gateway(InternetGatewayId=gateway.id)
            gateway.delete()

        # Flush all permissions, because if they refer to security group,
        # that security group won't be deleted
        log.info("Flushing permissions...")
        for sg in vpc.security_groups.all():
            if sg.ip_permissions:
                sg.revoke_ingress(IpPermissions=sg.ip_permissions)
            if sg.ip_permissions_egress:
                sg.revoke_egress(IpPermissions=sg.ip_permissions_egress)

        # Delete security groups themselves
        log.info("Deleting security groups...")
        for sg in vpc.security_groups.all():
            if sg.group_name != "default":
                sg.delete()

        log.info("Deleting VPC...")
        vpc.delete()

        log.info("Done destroying VPC %s", vpc_name)

    @classmethod
    def stop(cls, clusters, release_eip):
        if release_eip:
            log.info("The elastic IP(s) will be released as part of the stop process in order to reduce costs. "
                     "The next time the cluster is started, it will have a different IP. "
                     "Use --no-release-eip to retain the same IP(s) in between stop/start operations.")
            for cluster in clusters:
                cluster.release_eips()

        instances = [
            instance for cluster in clusters for instance in cluster.vpc.instances.all()
        ]

        log.info("Issuing stop request...")
        for instance in instances:
            instance.stop()

        log.info("Waiting until stopped...")
        for instance in instances:
            instance.wait_until_stopped()

    @classmethod
    def start(cls, clusters):
        head_nodes = []
        for c in clusters:
            if c.primary_head_node:
                head_nodes.append(c.primary_head_node)
            if c.secondary_head_node:
                head_nodes.append(c.secondary_head_node)

        log.info("Issuing start requests...")
        for head_node in head_nodes:
            head_node.start()

        log.info("Wait until started...")
        for head_node in head_nodes:
            head_node.wait_until_running()

        for cluster in clusters:
            cluster.assign_eips()

    @classmethod
    def find_some(cls, aws_session, prefix=None, names=None):
        if names:
            log.debug("Checking for name")
            # Check for duplicate names
            cnt = collections.Counter(names)
            duplicate_names = [name for name, count in cnt.items() if count > 1]
            if duplicate_names:
                raise UserReportableException(
                    "Duplicate cluster names: %s" % " ".join(duplicate_names))

            # Add prefix if present
            if prefix:
                names = ["%s-%s" % (prefix, name) for name in names]

            # Check if specified cluster exists
            all_clusters = list(Cluster.find(aws_session, names))
            all_cluster_names = [c.name for c in all_clusters]
            log.debug("Checking for matches in %s" % all_cluster_names)
            clusters = [
                cluster for cluster in all_clusters
                if cluster.name in names
            ]
            found_names = {cluster.name for cluster in clusters}

            # Use filtering instead of set operation here, to keep names order specified by user
            not_found_names = [name for name in names if name not in found_names]
            if not_found_names:
                raise CODException("Clusters not found: %s" % " ".join(not_found_names))

            return clusters
        elif prefix:
            log.debug("Checking for prefix %s" % prefix)
            return list(Cluster.find(aws_session, [prefix + "*"]))

        raise CODException("If you don't specify prefix, you need to specify cluster names")

    @classmethod
    def _is_main_routing_table(cls, route_table):
        for association in route_table.associations_attribute:
            if association.get("Main"):
                return True
        return False
