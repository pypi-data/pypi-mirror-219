async def gather(hub, profiles):
    """
    load k8s profiles from credential files

    Example:
    .. code-block:: yaml

        helm:
          profile_name:
            kube_config_path: '~/.kube/config'
            context: kubernetes-admin
    """
    sub_profiles = {}
    for profile, ctx in profiles.get("helm", {}).items():
        sub_profiles[profile] = ctx

    helm_profile = (hub.OPT.get("idem") or {}).get("acct_profile")
    if helm_profile not in sub_profiles:
        sub_profiles[helm_profile] = {"": ""}

    return sub_profiles
