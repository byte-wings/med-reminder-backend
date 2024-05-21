import uuid
import random
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken

MALE, FEMALE = ("male", "female")


class UserConfirmation(models.Model):
    """
    Model to store user verification codes and related information.
    """

    code = models.CharField(max_length=6)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        """
        Override the save method to set expiration time for phone verification codes.
        """
        if not self.pk:
            self.expiration_time = timezone.now() + timedelta(minutes=1)
        super(UserConfirmation, self).save(*args, **kwargs)


class User(AbstractBaseUser):
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
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_TYPE)
    phone_number = models.CharField(max_length=16, unique=True, validators=[_validate_phone])
    birth_date = models.DateField(blank=True, null=True)

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

