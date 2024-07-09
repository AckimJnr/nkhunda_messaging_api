def single_message_data(message):
    """
    retuns a single message
    """
    return {
        # "message_id": str(message["_id"]),
        "app_id": message["app_id"],
        "message_type": message["message_type"],
        "group_id": message["group_id"],
        "status": message["status"],
        "message_content": message["message_content"],
        "sender_id": message["sender_id"],
        "recipient_id": message["recipient_id"],
        "created_at": int(message["created_at"]),
        "updated_at": int(message["updated_at"])
    }

def all_messages_data(messages):
    """
    Returns a list of dictionaries of all messages
    """
    return [single_message_data(dict(message)) for message in messages]