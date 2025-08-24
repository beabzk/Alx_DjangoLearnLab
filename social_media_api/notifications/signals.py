
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Notification
from posts.models import Comment
from accounts.models import CustomUser

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.user,
            verb='liked your post',
            target=instance.post
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.author,
            actor=instance.author,
            verb='commented on your post',
            target=instance.post
        )

@receiver(post_save, sender=CustomUser.following.through)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.to_user,
            actor=instance.from_user,
            verb='started following you',
            target=instance.to_user
        )
