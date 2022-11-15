from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

MIN_AGE = 9
MAIL_LIST = ['rambler.ru']


def check_age_user(value: date):
    if relativedelta(date.today(), value).years < MIN_AGE:
        raise ValidationError(f'Your age is too young')


def check_email_address(value: str):
    value_split = value.split('@')
    if value_split[1] in MAIL_LIST:
        raise ValidationError(f'Your email is crazy')
