import uuid
import random
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.models import UserConfirmation

MALE, FEMALE = ("male", "female")


class UserManager(BaseUserManager):
    """
    Custom user manager for User model.
    """

    def create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a regular User with the given phone number and password."""
        if not phone_number:
            raise ValueError(_('The phone number must be set.'))

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('user_roles', SUPER_USER)
        return self._create_user(phone_number, password, **extra_fields)

    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError(_('The phone number must be set.'))

        user = self.model(phone_number=phone_number, username=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Custom user model with extended fields and methods.
    """
    _validate_phone = RegexValidator(
        regex=r"^998([378]{2}|(9[013-57-9]))\d{7}$",
        message="Your phone number must be connected with +9 and 12 characters! For example: 998998887766"
    )
    GENDER_TYPE = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=6, choices=GENDER_TYPE)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=16, unique=True, validators=[_validate_phone])
    birth_date = models.DateField(blank=True, null=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def create_verify_code(self):
        """
        Create and store a verification code for the user.
        """
        code = "".join(
            [str(random.randint(0, 100) % 10) for _ in range(6)])
        UserConfirmation.objects.create(
            user=self, code=code
        )
        return code

    def check_pass(self):
        if not self.password:
            temp_password = f"password{uuid.uuid4().__str__().split('-')[-1]}"
            self.password = temp_password

    def hashing_password(self):
        """
        Hash the password if not already hashed.
        """
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def tokens(self):
        """
        Generate JWT tokens for the user.
        """
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        super(User, self).save(*args, **kwargs)

    def clean(self):
        """
        Hash password the user.
        """
        self.check_pass()
        self.hashing_password()
