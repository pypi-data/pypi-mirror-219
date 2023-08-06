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
import typing

import tenacity

log = logging.getLogger("cluster-on-demand")


def delete_fs(efs_client, fs_id: str) -> None:
    log.debug(f"Deleting EFS: {fs_id}")
    try:
        efs_client.delete_file_system(FileSystemId=fs_id)
        _wait_resource_status(efs_client, "EFS", fs_id, describe_fs, "deleting", "deleted")
    except efs_client.exceptions.FileSystemNotFound:
        log.debug(f"EFS {fs_id} doesn't exists. Nothing to delete")


def delete_mount_target(efs_client, mount_target_id: str) -> None:
    log.debug(f"Deleting EFS mount target: {mount_target_id}")
    try:
        efs_client.delete_mount_target(MountTargetId=mount_target_id)
        _wait_resource_status(
            efs_client, "EFS mount target", mount_target_id, describe_mount_target, "deleting", "deleted"
        )
    except efs_client.exceptions.MountTargetNotFound:
        log.debug(f"EFS Mount target {mount_target_id} doesn't exists. Nothing to delete")


def describe_fs(
    efs_client,
    fs_id: typing.Optional[str] = None,
    *,
    token: typing.Optional[str] = None,
) -> typing.Optional[dict]:
    params = {}
    if fs_id:
        params["FileSystemId"] = fs_id
    elif token:
        params["CreationToken"] = token
    else:
        raise ValueError("Ether fs_id or token must be specified")

    response = efs_client.describe_file_systems(**params)
    file_systems = response["FileSystems"]

    if len(file_systems) > 1:
        raise Exception(f"Not expected to get more than one file system with parameters: {params}")
    return file_systems[0] if file_systems else None


def describe_mount_target(
    efs_client,
    mount_target_id: typing.Optional[str] = None,
    *,
    fs_id: typing.Optional[str] = None,
) -> dict:
    params = {}
    if mount_target_id:
        params["MountTargetId"] = mount_target_id
    elif fs_id:
        params["FileSystemId"] = fs_id
    else:
        raise ValueError("Ether mount_target_id or fs_id must be specified")

    response = efs_client.describe_mount_targets(**params)
    mount_targets = response["MountTargets"]
    if len(mount_targets) > 1:
        raise Exception(f"Not expected to get more than one mount target with parameters: {params}")
    return mount_targets[0] if mount_targets else None


def _wait_resource_status(efs_client, resource_type_name, resource_id, describer, current_status, expected_status):
    res_name = f"{resource_type_name} {resource_id}"

    # Unfortunately, boto3 doesn't have proper waiter for EFS client
    @tenacity.retry(
        wait=tenacity.wait_exponential(max=30),
        stop=tenacity.stop_after_delay(120),
        before_sleep=tenacity.before_sleep_log(log, logging.DEBUG),
        reraise=True,
        retry=tenacity.retry_if_exception_message(match=".*timed out to become.*"),
    )
    def wait():
        response = describer(efs_client, resource_id)
        status = response["LifeCycleState"]
        if status == current_status:
            raise Exception(f"{res_name} timed out to become {expected_status}")
        if status != expected_status:
            raise Exception(f"{res_name} went into unexpected status {status}. Expected {expected_status}")
        return response

    log.debug(f"Waiting for {res_name} to become {expected_status}")
    return wait()
