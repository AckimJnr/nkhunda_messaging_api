def single_message_data(message):
    """
    retuns a single message
    """
    return {
        # "message_id": str(message["_id"]),
        "app_id": message["app_id"],
        "message_type": message.get("message_type", None),
        "group_id": message.get("group_id", None),
        "status": message.get("status", None),
        "message_content": message.get("message_content", None),
        "sender_id": message.get("sender_id", None),
        "recipient_id": message.get("recipient_id", None),
        "created_at": int(message["created_at"]),
        "updated_at": int(message["updated_at"])
    }

def all_messages_data(messages):
    """
    Returns a list of dictionaries of all messages
    """
    return [single_message_data(dict(message)) for message in messages]