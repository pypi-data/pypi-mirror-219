from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CreatedUpdatedMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The creation time, always in UTC timezone."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("The last update time, always in UTC timezone."),
    )


class Category(CreatedUpdatedMixin):
    """Stores the categories of notifications"""

    title = models.CharField(max_length=30)
    icon = models.ImageField(upload_to="category/icons", null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Notification(CreatedUpdatedMixin):
    """Stores the in app notifications of project"""

    class NotificationType(models.TextChoices):
        success = "success", _("Success")
        error = "error", _("Error")
        warning = "warning", _("Warning")
        info = "info", _("Information")

    class NotificationState(models.TextChoices):
        read = "read", _("Read")
        unread = "unread", _("Unread")
        deleted = "deleted", _("Deleted")

    title = models.CharField(max_length=265)
    message = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    receivers = models.ManyToManyField(User, related_name="receivers_notifications")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(
        choices=NotificationType.choices, max_length=20
    )
    state = models.CharField(
        choices=NotificationState.choices,
        max_length=20,
        default=NotificationState.unread,
    )

    def __str__(self) -> str:
        return self.title
