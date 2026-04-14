def single_message_data(message) -> dict:
    """
    Returns a serialized dictionary of a single message.
    message_id is included so clients can reference messages by ID.
    """
    return {
        "message_id": str(message["_id"]),
        "app_id": message.get("app_id"),
        "message_type": message.get("message_type"),
        "group_id": message.get("group_id"),
        "status": message.get("status"),
        "message_content": message.get("message_content"),
        "sender_id": message.get("sender_id"),
        "recipient_id": message.get("recipient_id"),
        "created_at": int(message["created_at"]),
        "updated_at": int(message["updated_at"]),
    }


def all_messages_data(messages) -> list:
    """
    Returns a list of serialized message dictionaries.
    """
    return [single_message_data(dict(message)) for message in messages]