from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField

class UserProfile(models.Model):
    """
    A user profile model for maintaining default delivery information
    and order history.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model.
        default_phone_number (CharField): The default phone number of the user.
        default_country (CountryField): The default country of the user.
        default_postcode (CharField): The default postal code of the user.
        default_town_or_city (CharField): The default town or city of the user.
        default_street_address1 (CharField): The first line of the default 
                                            street address of the user.
        default_street_address2 (CharField): The second line of the default 
                                            street address of the user.
        default_county (CharField): The default county of the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    default_country = CountryField(
        blank_label='Country *', null=True, blank=True)
    default_postcode = models.CharField(
        max_length=20, null=True, blank=True)
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True)
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(
        max_length=80, null=True, blank=True)
    default_county = models.CharField(
        max_length=80, null=True, blank=True)

    def __str__(self):
        """
        String representation of the UserProfile model.

        Returns:
            str: The username of the associated User.
        """
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile.

    If a User instance is created, this function creates a UserProfile 
    instance associated with the User. For existing User instances, 
    it saves the associated UserProfile instance.

    Args:
        sender (Model class): The model class that sent the signal.
        instance (User): The instance of the User model that triggered the signal.
        created (bool): A boolean indicating whether the User instance was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
