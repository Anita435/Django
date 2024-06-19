import uuid
import jwt

from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.postgres.fields import ArrayField, JSONField

from model_utils.models import TimeStampedModel
from .managers import ModelManager
from .mixin import StatusMixin
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    '''
    creating a manager for a custom user model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
    '''

    def create_user(self, email, phone_number, password=None, age=None):
        """Create and return a `User` with an email, username and password."""
        if phone_number is None:
            raise TypeError('Users must have a Phone number.')

        # if email is None:
        #     raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), phone_number=phone_number, age=age)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email,phone_number, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, phone_number, password, age=None)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    # username = models.CharField(db_index=True, max_length=255, unique=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(null=True,blank=True,default=None)

    # When a user no longer wishes to use our platform, they may try to delete
    # their account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. We
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # false.
    is_staff = models.BooleanField(default=False)

    # Verify OTP or not for ever user
    otp_verify = models.BooleanField(default=False)

    # email verify or not for ever user
    email_verify = models.BooleanField(default=False)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False)
    age = models.CharField(max_length=3, null=True, blank=True)

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        if self.email:
            return self.email
        elif self.phone_number:
            return self.phone_number
        else:
            return str(self.id)

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        token ,created = Token.objects.get_or_create(user=self)
        return token.key

    # def _generate_jwt_token(self):
    #     """
    #     Generates a JSON Web Token that stores this user's ID and has an expiry
    #     date set to 60 days into the future.
    #     """
    #     dt = datetime.now() + timedelta(days=2)

    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')

    #     return token.decode('utf-8')

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "User"


class UserProfile(TimeStampedModel, StatusMixin):
    first_name = models.CharField('FirstName',max_length=100,null=True,blank=True)
    last_name = models.CharField('LastName',max_length=100,null=True,blank=True)
    user = models.ForeignKey("User", blank=True, null=True,
                             on_delete=models.CASCADE, related_name='user_profile')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ("O", 'Other')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    objects = ModelManager()

    class Meta:
        verbose_name = "User Profile Details"
        verbose_name_plural = "User Profile Details"


class OTPDetails(TimeStampedModel, StatusMixin):
    otp_response = JSONField(null=True,blank=True)
    user = models.ForeignKey("User", blank=True, null=True,
                             on_delete=models.CASCADE, related_name='user_profile_otp')

    class Meta:
        verbose_name = "OTP Detail"
        verbose_name_plural = "OTP Details"


class UserLoginActivity(models.Model):
    # Login Status
    SUCCESS = 'S'
    FAILED = 'F'

    LOGIN_STATUS = ((SUCCESS, 'Success'),
                    (FAILED, 'Failed'))

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField(auto_now=True)
    login_username = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=1, default=SUCCESS, choices=LOGIN_STATUS, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'user_login_activity'
        verbose_name_plural = 'user_login_activities'
