def single_org_data(org):
    """
    Returns a dictionary of a single organisation
    """
    return {
        "org_id": str(org["_id"]),
        "name": org.get("name", None),
        "apps": org.get("apps", None),
        "token": org.get("token", None),
        "created_at": int(org["created_at"]),
        "updated_at": int(org["updated_at"])
    }

def all_orgs_data(orgs):
    """
    Returns a list of dictionaries of all organisations
    """
    return [single_org_data(org) for org in orgs]