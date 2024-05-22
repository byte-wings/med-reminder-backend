import phonenumbers
from rest_framework.exceptions import ValidationError


def phone_checker(p_number):
    if not (p_number and isinstance(p_number, str) and p_number.isdigit()):
        raise ValidationError("phone_number is not valid")


def phone_parser(p_number, c_code=None):
    try:
        phone_checker(p_number)
        p_number = '+' + p_number
        return phonenumbers.parse(p_number, c_code)
    except Exception as e:
        raise ValidationError("Phone number is not valid")
