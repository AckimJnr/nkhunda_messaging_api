"""
Contains data definition for user model
"""

def single_user_data(user):
    """
    Returns a dictionary of a single user
    """
    return {
        "user_id": str(user["_id"]),
        "org_id": user.get("org_id", None),
        "app_id": user.get("app_id", None),
        "full_name": user.get("full_name", None),
        "email": user.get("email", None),
        "role": user.get("role", None),
        "created_at": int(user["created_at"]),
        "updated_at": int(user["updated_at"])
    }

def all_users_data(users):
    """
    Returns a list of dictionaries of all users
    """
    return [single_user_data(user) for user in users]
