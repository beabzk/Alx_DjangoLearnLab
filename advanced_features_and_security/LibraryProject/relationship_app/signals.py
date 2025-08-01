from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import UserProfile

# Get the custom user model
User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # This signal ensures the profile is saved whenever the user is saved.
    # It handles both creation and updates.
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # This handles the case for existing users that don't have a profile yet
        UserProfile.objects.create(user=instance)