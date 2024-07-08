from datetime import datetime

def send_message(message_data):
    """
    Function that processess sent messages
    """
    message = {}
    try:
        print(f"Sending message: {message_data}")
        message = {
            "app_id": message_data["app_id"],
            "message_type": message_data["message_type"],
            "group_id": message_data["group_id"],
            "status": message_data["status"],
            "message_content": message_data["message_content"],
            "sender_id": message_data["sender_id"],
            "recipient_id": message_data["recipient_id"],
            "created_at": message_data.get("created_at", int(datetime.timestamp(datetime.now()))),
            "updated_at": int(datetime.timestamp(datetime.now())),
        }

        return message
    except Exception as e:
        print(f"Error sending message: {e}")
        return {"status": "failure", "error": str(e)}
