import re

from django.core.exceptions import ValidationError


def validate_phone_number(value: str) -> None:
    """
    Принимает номера в международном формате: +996550172225
    Правило: знак '+', затем от 7 до 15 цифр (ITU-T E.164).
    """
    pattern = re.compile(r'^\+[1-9]\d{6,14}$')
    if not pattern.match(value.strip()):
        raise ValidationError(
            'Введите номер в международном формате: +996XXXXXXXXX'
        )
