def single_app_data(app):
    """
    Returns a dictionary of a single app
    """
    return {
        "app_id": str(app["_id"]),
        "org_id": app["org_id"],
        "users": app["users"],
        "app_name": app["app_name"],
        "app_type": app["app_type"],
        "app_description": app["app_description"],
        "groups": app["groups"],
        "created_at": int(app["created_at"]),
        "updated_at": int(app["updated_at"])
    }

def all_apps_data(apps):
    """
    Returns a list of dictionaries of all apps
    """
    return [single_app_data(app) for app in apps]
