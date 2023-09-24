from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_ws_message_to_user_group(user, message_type, data):
    """
    Sends a WebSocket message to a user's group.

    Args:
        user (User): The user to send the message to.
        message_type (str): The message type (e.g., "card_update"). This will be used to recognize the function in consumer and event in .js
        data (dict): The data to send in the message.

    Returns:
        None
    """
    channel_layer = get_channel_layer()
    email = str(user).replace("@", "_").replace(".", "_")

    async_to_sync(channel_layer.group_send)(
        f"user_{email}", # The channel group which is the users email
        {
            "type": message_type,
            "card": data,
        }
    )