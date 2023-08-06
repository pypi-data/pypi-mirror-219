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

import logging
import re
from datetime import datetime

from clusterondemand.images.find import CODImage, ImageSource
from clusterondemand.images.find import findimages_ns as common_findimages_ns
from clusterondemandconfig import ConfigNamespace, config

from .ec2connection import create_ec2_resource_client, establish_connection_to_aws

log = logging.getLogger("cluster-on-demand")

findimages_ns = ConfigNamespace("aws.images.find", help_section="image filter parameters")
findimages_ns.import_namespace(common_findimages_ns)
findimages_ns.override_imported_parameter("cloud_type", default="aws")
findimages_ns.add_parameter(
    "image_owner",
    default="137677339600",
    help="AWS account ID of the account containing the head node image(s). "
         "Defaults to the ID of the official AWS account of Bright Computing. "
         "Related parameter: --image-visibility .",
)
IMAGE_NAME_REGEX_AWS = r"^(?:bright[^-]+)-([^-]+(?:-dev)?)-([^-]+)-hvm-(.*)$"


class CannotParseImageName(Exception):
    pass


class AWSImageSource(ImageSource):
    @classmethod
    def from_config(cls, config, ids=None):
        return AWSImageSource(
            ids=ids if ids is not None else config["ids"],
            version=config["version"],
            distro=config["distro"],
            status=config["status"],
            advanced=True,
            image_visibility=config["image_visibility"],
            cloud_type=config["cloud_type"],
        )

    def _iter_from_source(self):
        allow_custom_images = False
        image_owners = []
        image_ids = []
        filters = []

        if self.uuids:
            # Find images by AMI ids. They might be non-Bright
            image_ids = self.uuids[:]
            allow_custom_images = True
        else:
            image_owners = [config["image_owner"]]

            filters = [
                {"Name": "name", "Values": ["brightheadnode-*"]},
            ]

            if config["image_visibility"] == "public":
                filters += [{"Name": "is-public", "Values": ["true"]}]
            elif config["image_visibility"] == "private":
                filters += [{"Name": "is-public", "Values": ["false"]}]
            elif config["image_visibility"] == "any":
                # not specifying a filter will result in both public and private be fetched
                pass

        ec2, _ = create_ec2_resource_client(establish_connection_to_aws())
        images = list(ec2.images.filter(Owners=image_owners, Filters=filters, ImageIds=image_ids))

        for image in images:
            try:
                cod_image = make_cod_image_from_aws(image, allow_custom_images=allow_custom_images)
            except CannotParseImageName as e:
                # This is parsing names of public images, someone could even upload some bogus name
                # to break our code. So we just ignore if we can't parse it
                # Other exception can blow up
                log.debug(e)
            else:
                yield cod_image


def make_cod_image_from_aws(amazon_image, allow_custom_images=False):
    """
    Convert boto3's image object to COD image object

    :param amazon_image: boto3.resource image object
    :param allow_custom_images: allow non-Bright images
    :return: CODImage object for specified image
    """
    additional_params = {}
    match = re.match(IMAGE_NAME_REGEX_AWS, amazon_image.name)
    if match:
        version, distribution, revision = match.groups()
        additional_params = {
            "version": version,
            "distro": distribution,
            "revision": int(revision),
            "id": f"{distribution}-{version}",
        }
    elif not allow_custom_images:
        raise CannotParseImageName(f"Cannot parse image name {amazon_image.name}")

    return CODImage(
        name=amazon_image.name,
        uuid=amazon_image.id,
        created_at=datetime.fromisoformat(amazon_image.creation_date.replace("Z", "+00:00")),
        image_visibility="public" if amazon_image.public else "private",
        type="headnode",
        cloud_type="aws",
        **additional_params,
    )
