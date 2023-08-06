from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models import F

from notifications.models import Category, Notification

User = get_user_model()


def send_notification(
    title: str,
    receivers: list[User],
    notification_type: str,
    sender: User = None,
    message: str = None,
    category: Category = None,
    real_time_notification: bool = True,
):
    """This function will send in app notification.

    Parameters:
    1. title : string
    2. receivers : List of User model instance
    3. sender : User model instance
    4. notification_type :
        a. success
        b. error
        c. warning
        d. info
    5. message : string
    6. category : Category Model instance
    7. notification_status :
        a. read
        b. unread
        c. deleted
    8. real_time_notification : bool (Set True if you want to implement Real Time Notifications)
    """
    if len(receivers) == 0:
        return "Please provide atleast one receiver."
    if notification_type not in list(
        dict(Notification.NotificationType.choices).keys()
    ):
        return f"Please provide valid notification type. It should be any of {list(dict(Notification.NotificationType.choices).keys())}."

    notification = Notification.objects.create(
        title=title,
        message=message,
        category=category,
        sender=sender,
        notification_type=notification_type,
        state=Notification.NotificationState.unread,
    )
    for receiver in receivers:
        notification.receivers.add(receiver)

    if real_time_notification:
        channel_layer = get_channel_layer()
        # Trigger message sent to group
        for receiver in receivers:
            async_to_sync(channel_layer.group_send)(
                f"notifications_{receiver.pk}",  # Group Name, Should always be string
                {
                    "type": "notify",  # Custom Function written in the consumers.py
                    "content": [
                        {
                            "title": title,
                            "message": message,
                            "notification_type": notification.get_notification_type_display(),
                            "category_type": category.title if category else "",
                            "sender_name": sender.username if sender else "",
                        }
                    ],
                    "command": "new_notification",
                },
            )
    return "Notification sent successfully."


def get_notifications(user, notification_type=None):
    if not notification_type:
        return (
            Notification.objects.prefetch_related("receivers")
            .filter(receivers=user)
            .annotate(
                sender_name=F("sender__username"), category_type=F("category__title")
            )
            .values(
                "title", "message", "notification_type", "sender_name", "category_type"
            )
        )

    if notification_type not in list(
        dict(Notification.NotificationType.choices).keys()
    ):
        return f"Please provide valid notification type. It should be any of {list(dict(Notification.NotificationType.choices).keys())}."
    else:
        return (
            Notification.objects.prefetch_related("receivers")
            .filter(receivers=user, notification_type=notification_type)
            .annotate(
                sender_name=F("sender__username"), category_type=F("category__title")
            )
            .values(
                "title", "message", "notification_type", "sender_name", "category_type"
            )
        )


def mark_as_read(user):
    Notification.objects.filter(
        receivers=user, state=Notification.NotificationState.unread
    ).update(state=Notification.NotificationState.read)

    return f"Notifications of user {user} marked as read."


def mark_as_unread(user):
    Notification.objects.filter(
        receivers=user, state=Notification.NotificationState.read
    ).update(state=Notification.NotificationState.unread)
    return f"Notifications of user {user} marked as unread."
