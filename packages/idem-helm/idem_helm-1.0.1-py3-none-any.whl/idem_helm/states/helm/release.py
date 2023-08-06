"""States module for Helm Release."""
import copy
import re
from typing import Any
from typing import Dict
from typing import List

import dict_tools.differ as differ
import yaml

__contracts__ = ["resource", "soft_fail"]


async def present(
    hub,
    ctx,
    name: str,
    chart: str,
    namespace: str,
    repository: str = None,
    resource_id: str = None,
    values: Dict = None,
    version: str = None,
    key_file: str = None,
    keyring: str = None,
    ca_file: str = None,
    cert_file: str = None,
    username: str = None,
    password: str = None,
    values_files: List = None,
    dependency_update: bool = False,
    create_namespace: bool = False,
    atomic: bool = False,
    devel: bool = False,
    disable_openapi_validation: bool = False,
    no_hooks: bool = False,
    verify: bool = False,
    timeout: str = None,
) -> Dict[str, Any]:
    """Create/Update a Helm Release.

    Args:
        name(str): An Idem name of the resource.
        chart(str): Chart name to be installed
        namespace(str): namespace scope for helm release
        resource_id(str, Optional): An identifier of the resource in the provider.
        repository(str, Optional): chart repository url where to locate the requested chart
        values(Dict, Optional): Specify values in a YAML
        version(str, Optional): Chart version to install. If this is not specified, the latest version is installed.
        key_file(str, Optional): The repositories cert key file
        keyring(str, Optional): location of public keys used for verification (default "~/.gnupg/pubring.gpg")
        values_files(List, Optional): specify values in a YAML file
        ca_file(str, Optional): verify certificates of HTTPS-enabled servers using this CA bundle
        cert_file(str, Optional): identify HTTPS client using this SSL certificate file
        username(str, Optional): chart repository username where to locate the requested chart
        password(str, Optional): chart repository password where to locate the requested chart
        dependency_update(bool, Optional): update dependencies if they are missing before installing the chart
        create_namespace(bool, Optional): create the release namespace if not present
        atomic(bool, Optional): if True, the installation process deletes the installation on failure.
        devel(bool, Optional): use development versions, too. Equivalent to version '>0.0.0-0'. If --version is set, this is ignored
        disable_openapi_validation(bool, Optional): if set, the installation process will not validate rendered templates against the Kubernetes OpenAPI Schema
        no_hooks(bool, Optional): prevent hooks from running during install
        verify(bool, Optional): verify the package before using it.
            If verify is set, the chart MUST have a provenance file, and the provenance file MUST pass all verification steps.
        timeout(str, Optional): time to wait for Kubernetes commands to complete. (Ex-: 100s, 200s, 10m)

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem-helm-release-test:
              helm.release.present:
                - name: idem-redis
                - resource_id: idem-redis
                - repository: https://charts.bitnami.com/bitnami
                - chart: redis
                - namespace: kube-system
                - timeout: 200s

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    before = None
    list_release_ret = None
    # Check for existing release by name in namespace
    if resource_id:
        list_release_ret = await hub.exec.helm.release.list_releases(
            ctx, resource_id, namespace
        )
        if not list_release_ret["result"] or not list_release_ret["ret"]:
            result["comment"] = list_release_ret["comment"]
            result["result"] = False
            return result

    # Update current state
    if list_release_ret and list_release_ret["ret"]:
        current_state = list_release_ret["ret"][0]
        current_value_ret = await hub.exec.helm.release.get_release_values(
            ctx, current_state
        )

        if not current_value_ret["result"]:
            result["comment"] = current_value_ret["comment"]
            result["result"] = False
            return result

        before = hub.tool.helm.release_utils.convert_raw_release_to_present(
            release_metadata=current_state, release_values=current_value_ret["ret"]
        )
        result["old_state"] = before

    # Handle no change behaviour
    # Since the repository attributes and other flags are not being persisted as metadata by helm, it will not be set to any value.
    desired_state = {
        "resource_id": resource_id,
        "chart": chart + (("-" + version) if version else ""),
        "namespace": namespace,
        "values": values,
        "name": name,
        "values_files": values_files,
    }

    try:
        is_change_detected = await __is_update_required(
            desired_state, result["old_state"]
        )
    except yaml.YAMLError as exception:
        result["comment"] = result["comment"] + (str(exception),)
        result["result"] = False
        return result

    if not is_change_detected:
        result["comment"] = hub.tool.helm.comment_utils.already_exists_comment(
            resource_type="helm.release", name=name
        )
        result["new_state"] = copy.deepcopy(result["old_state"])
        return result

    # Handle test behaviour
    if ctx.get("test", False):
        result["new_state"] = hub.tool.helm.test_state_utils.generate_test_state(
            enforced_state=before,
            desired_state=desired_state,
        )
        result["comment"] = (
            hub.tool.helm.comment_utils.would_update_comment(
                resource_type="helm.release", name=name
            )
            if before
            else hub.tool.helm.comment_utils.would_create_comment(
                resource_type="helm.release", name=name
            )
        )
        return result

    kvflags = {
        "namespace": namespace,
        "set": values,
        "version": version,
        "repo": repository,
        "key-file": key_file,
        "keyring": keyring,
        "ca-file": ca_file,
        "cert-file": cert_file,
        "values": values_files,
        "username": username,
        "password": password,
        "timeout": timeout,
    }
    flags = []

    if dependency_update:
        flags.append("dependency-update")
    if create_namespace:
        flags.append("create-namespace")
    if atomic:
        flags.append("atomic")
    if devel:
        flags.append("devel")
    if disable_openapi_validation:
        flags.append("disable-openapi-validation")
    if no_hooks:
        flags.append("no-hooks")
    if verify:
        flags.append("verify")

    # Handle actual resource create or update
    if before:
        upgrade_ret = await hub.exec.helm.release.upgrade_release(
            ctx, name, chart, flags, kvflags
        )
        if not upgrade_ret["result"]:
            result["comment"] = upgrade_ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.helm.comment_utils.update_comment(
            resource_type="helm.release", name=name
        )
    else:
        install_ret = await hub.exec.helm.release.install_release(
            ctx, name, chart, flags, kvflags
        )
        if not install_ret["result"]:
            created = False
            if (
                "the server is currently unable to handle the request"
                in install_ret["comment"]
            ):
                list_release_ret = await hub.exec.helm.release.list_releases(
                    ctx, name, namespace
                )
                if list_release_ret["result"] and list_release_ret["ret"]:
                    created = True

            if not created:
                result["comment"] = install_ret["comment"]
                result["result"] = False
                return result
        result["comment"] = hub.tool.helm.comment_utils.create_comment(
            resource_type="helm.release", name=name
        )
        resource_id = name
        # creation was successful, set resource_id so that we get resource_id from esm even if fetching updated
        # resource fails.
        result["new_state"] = {"resource_id": resource_id}

    # Fetch the updated resource and update new_state
    list_release_ret = await hub.exec.helm.release.list_releases(
        ctx, resource_id, namespace
    )

    if not list_release_ret["result"] or not list_release_ret["ret"]:
        result["comment"] = result["comment"] + list_release_ret["comment"]
        result["result"] = False
        return result

    after = list_release_ret["ret"][0]

    value_ret = await hub.exec.helm.release.get_release_values(ctx, after)
    if not value_ret["result"]:
        result["comment"] = result["comment"] + value_ret["comment"]
        result["result"] = False
        return result

    result["new_state"] = hub.tool.helm.release_utils.convert_raw_release_to_present(
        release_metadata=after, release_values=value_ret["ret"]
    )
    return result


async def __is_update_required(desired_state, old_state):
    if not old_state:
        return True
    if desired_state.get("values_files"):
        if not desired_state.get("values"):
            desired_state["values"] = {}
        for values_file in desired_state.get("values_files"):
            with open(values_file) as stream:
                data = yaml.safe_load(stream)
            desired_state["values"].update(data)
        desired_state["values_files"] = None

    __merge_arguments(desired_state.get("values"), old_state.get("values"))

    diff = differ.deep_diff(old_state, desired_state)
    is_change_detected = False
    for item in diff["new"]:
        new_value = diff["new"].get(item)
        if new_value:  # if value is not None
            if item == "chart":
                old_val = diff["old"].get("chart")
                is_change_detected = not (
                    old_val.startswith(new_value)
                    and re.search(r"-(\d+\.)?(\d+\.)?(\*|\d+)$", old_val)
                )
            elif (item == "values" or item == "values_files") and desired_state.get(
                "values_files"
            ):
                continue
            else:
                is_change_detected = True
    return is_change_detected


def __merge_arguments(desire_state: Dict[str, Any], current_state: Dict[str, Any]):
    """
    Assign current_state values to desire_state if desire_state value is None
    or parameter key is missing in desire_state.
    """
    if not desire_state and current_state:
        desire_state = copy.deepcopy(current_state)
        return desire_state

    if isinstance(current_state, dict):
        for key, value in current_state.items():
            if key in desire_state:
                desire_value = desire_state.get(key)
                if desire_value is None:
                    desire_state[key] = value
                elif isinstance(desire_value, dict):
                    desire_state[key] = __merge_arguments(desire_value, value)
            else:
                desire_state[key] = value

    return desire_state


async def absent(
    hub, ctx, name: str, namespace: str = "default", resource_id: str = None
) -> Dict[str, Any]:
    """Delete a helm release

    Args:
        name(str): An Idem name of the resource.
        namespace(str, Optional): namespace scope for helm release.
            Defaults to 'default' namespace, in case of value not provided in absent state.
        resource_id(str, Optional): An identifier of the resource in the provider.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem-helm-release-test:
              helm.release.absent:
                - name: idem-redis
                - resource_id: idem-redis
                - namespace: kube-system

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    before = None
    if resource_id:
        list_release_ret = await hub.exec.helm.release.list_releases(
            ctx, resource_id, namespace
        )
        if list_release_ret["ret"]:
            value_ret = await hub.exec.helm.release.get_release_values(
                ctx, list_release_ret["ret"][0]
            )
            before = hub.tool.helm.release_utils.convert_raw_release_to_present(
                release_metadata=list_release_ret["ret"][0],
                release_values=value_ret["ret"],
            )
            result["old_state"] = before

    if not before:
        result["comment"] = hub.tool.helm.comment_utils.already_absent_comment(
            resource_type="helm.release", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.helm.comment_utils.would_delete_comment(
            resource_type="helm.release", name=name
        )
    else:
        cmd_ret = await hub.exec.helm.release.uninstall_release(ctx, name, namespace)
        if not cmd_ret["result"]:
            result["comment"] = cmd_ret["comment"]
            result["result"] = False
            return result

        result["comment"] = hub.tool.helm.comment_utils.delete_comment(
            resource_type="helm.release", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """list of helm releases in all namespaces.

    Repository attributes and other flags are not being persisted as metadata by helm,
    it will not be set to any value by default.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe helm.release

    """
    list_release_ret = await hub.exec.helm.release.list_releases(ctx)
    if not list_release_ret["result"]:
        hub.log.debug(f"Could not describe helm release {list_release_ret['comment']}")
        return {}

    all_releases = list_release_ret["ret"]
    result = {}
    for release in all_releases:
        resource_id = release["name"]
        value_ret = await hub.exec.helm.release.get_release_values(ctx, release)
        if not value_ret["result"]:
            hub.log.debug(
                f"Could not describe values for helm release {resource_id} : {value_ret['comment']}"
            )
            continue

        release_resource = hub.tool.helm.release_utils.convert_raw_release_to_present(
            release_metadata=release, release_values=value_ret["ret"]
        )
        result[resource_id] = {
            "helm.release.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in release_resource.items()
            ]
        }

    return result
