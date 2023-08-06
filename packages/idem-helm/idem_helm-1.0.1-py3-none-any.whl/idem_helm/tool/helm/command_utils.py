import copy
import os
import re
from collections.abc import MutableMapping


class HelmConfigurationError(Exception):
    def __init__(self, message="kube_config_path need to be set"):
        self.message = message
        super().__init__(self.message)


def prepare_command(hub, ctx, commands=None, flags=None, kvflags=None, value_file=None):
    if commands is None:
        commands = []
    if flags is None:
        flags = []
    else:
        flags = copy.deepcopy(flags)
    if kvflags is None:
        kvflags = {}
    else:
        kvflags = copy.deepcopy(kvflags)

    cmd = ("helm",)

    config_file_path, context = hub.tool.helm.command_utils.get_kube_config_and_context(
        ctx
    )

    kvflags.update({"kubeconfig": config_file_path})

    # If context is None, helm command uses current_context from config file.
    if context:
        kvflags.update({"kube-context": context})

    for command in commands:
        cmd += (command,)

    for arg in flags:
        if not re.search(r"^--.*", arg):
            arg = "--" + arg
        cmd += (arg,)

    for key, val in kvflags.items():
        if val is None:
            continue

        if not re.search(r"^--.*", key):
            key = "--" + key

        if key == "--set" or key == "--values":
            if value_file:
                cmd += (
                    "--values",
                    value_file,
                )
            else:
                cmd = __set_values(cmd, key, val)
        else:
            cmd += (
                key,
                val,
            )

    return cmd


def get_kube_config_and_context(hub, ctx):
    config_file_path = os.environ.get("KUBE_CONFIG_PATH")
    context = os.environ.get("KUBE_CTX")
    helm_profile = (hub.OPT.get("idem") or {}).get("acct_profile")

    if not config_file_path:
        config_file_path = (
            (((hub.OPT.get("acct") or {}).get("extras") or {}).get("helm") or {}).get(
                helm_profile
            )
            or {}
        ).get("kube_config_path")

    if not context:
        context = (
            (((hub.OPT.get("acct") or {}).get("extras") or {}).get("helm") or {}).get(
                helm_profile
            )
            or {}
        ).get("context")

    if not config_file_path:
        config_file_path = ctx.acct.get("kube_config_path")

    if not context:
        context = ctx.acct.get("context")

    if not config_file_path:
        raise HelmConfigurationError

    config_file_path = (
        os.path.expanduser(config_file_path)
        if "~" in config_file_path
        else config_file_path
    )
    return config_file_path, context


def __set_values(cmd, key, val):
    values = __flatten_values(val, sep=".") if key == "--set" else val
    if isinstance(values, list):
        for value in values:
            cmd += (
                key,
                value,
            )
    else:
        cmd += (
            key,
            values,
        )
    return cmd


def __flatten_values(d, parent_key="", sep="."):
    if not d:
        return
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            val = __flatten_values(v, new_key, sep=sep)
            if val:
                items.extend(val)
        else:
            items.append(new_key + "=" + str(v))
    return items
