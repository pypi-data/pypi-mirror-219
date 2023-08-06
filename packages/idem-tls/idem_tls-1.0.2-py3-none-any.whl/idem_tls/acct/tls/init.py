async def gather(hub, profiles):
    """
    load tls profiles from credential files

    Example:
    .. code-block:: yaml

        tls:
          default:
            method: TLSv1_2
    """
    sub_profiles = {}
    for profile, ctx in profiles.get("tls", {}).items():
        sub_profiles[profile] = ctx

    tls_profile = (hub.OPT.get("idem") or {}).get("acct_profile")
    if tls_profile not in sub_profiles:
        sub_profiles[tls_profile] = {"": ""}

    return sub_profiles
