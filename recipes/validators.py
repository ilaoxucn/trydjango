from django.core.exceptions import ValidationError

valid_unit_measurements = ['个','克','千克','袋']

def validate_unit_of_measure(value):
    if value not in valid_unit_measurements:
        raise ValidationError(f"{value}不是一个合理的单位")
