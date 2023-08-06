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


from __future__ import absolute_import, print_function

import logging

import boto3
from botocore.exceptions import ClientError

from clusterondemand.exceptions import CODException, UserReportableException
from clusterondemandconfig import config

log = logging.getLogger("cluster-on-demand")


PRODUCTS_FILTER = [
    {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": "Linux"},
    {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": "NA"},
    {"Type": "TERM_MATCH", "Field": "tenancy", "Value": "Shared"},
]

PRODUCT_FAMILIES = [
    {"Type": "TERM_MATCH", "Field": "productFamily", "Value": "Compute Instance"}
]


def list_regions():
    """Return a list of available regions in an AWS subscription."""
    aws_key_id = config["aws_access_key_id"]
    aws_secret = config["aws_secret_key"]
    region_name = config["aws_region"] or "eu-west-1"
    try:
        log.debug(f"Using '{region_name}' endpoint to list regions")
        ec2_client = boto3.client(
            "ec2", region_name=region_name,
            aws_access_key_id=aws_key_id,
            aws_secret_access_key=aws_secret
        )
        regions = ec2_client.describe_regions()["Regions"]
        region_names = [region["RegionName"] for region in regions]
        return region_names
    except ClientError as e:
        if "AWS was not able to validate the provided access credentials" in str(e):
            raise UserReportableException("The provided AWS credentials were invalid.")
        raise CODException("Error listing AWS regions", caused_by=e)


def get_available_instance_types(region):
    ec2_client = boto3.client(
        "ec2",
        region_name=region,
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_key"],
    )

    log.info(f"Finding instance types for region: {region}")
    instance_types = []
    paginator = ec2_client.get_paginator("describe_instance_types")
    filters = [{"Name": "supported-virtualization-type", "Values": ["hvm"]}]
    for page in paginator.paginate(Filters=filters):
        for instance_type_definition in page.get("InstanceTypes"):
            instance_types.append(instance_type_definition.get("InstanceType"))

    return instance_types
