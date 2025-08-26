import re
from datetime import date

from django.core.exceptions import ValidationError


def validate_future_date(value):
    if value > date.today():
        raise ValidationError("Дата не может быть в будущем")


def validate_sire(child, sire):
    if child == sire:
        raise ValidationError("Мать и ребёнок не могут совпадать")
    if sire.sex != 0:
        raise ValidationError("Мать не может быть жеребцом или мерином")

    selected_sire = child.parents.filter(sex=0).first()
    if selected_sire:
        raise ValidationError(f"Мать {child}: {selected_sire}")

    if child.bdate and sire.bdate:
        child_bdate = child.bdate
        sire_bdate = sire.bdate

        if child.bdate_mode == 1 or sire.bdate_mode == 1:
            child_bdate.replace(month=1, day=1)
            sire_bdate.replace(month=1, day=1)

        if child.bdate_mode == 2 or sire.bdate_mode == 2:
            child_bdate.replace(day=1)
            sire_bdate.replace(day=1)

        if child_bdate > sire_bdate:
            raise ValidationError("Дата рождения матери не может быть "
                                  "больше даты рождения лошади")

        if sire.ddate:
            sire_ddate = sire.ddate
            child_bdate = child.bdate

            if child.bdate_mode == 1 or sire.ddate_mode == 1:
                child_bdate.replace(month=1, day=1)
                sire_ddate.replace(month=1, day=1)

            if child.bdate_mode == 2 or sire.ddate_mode == 2:
                child_bdate.replace(day=1)
                sire_ddate.replace(day=1)

            if sire_ddate < child_bdate:
                raise ValidationError("Дата смерти матери не может быть "
                                      "раньше даты рождения лошади")


def validate_dame(child, dame):
    if child == dame:
        raise ValidationError("Мать и отец не могут совпадать")

    if dame.sex == 0:
        raise ValidationError("Отец не может быть кобылой")

    selected_dame = child.parents.filter(sex__in=[1, 2]).first()
    if selected_dame:
        raise ValidationError(f"Отец {child}: {selected_dame}")

    if child.bdate and dame.bdate:
        child_bdate = child.bdate
        dame_bdate = dame.bdate

        if child.bdate_mode == 1 or dame.bdate_mode == 1:
            child_bdate.replace(month=1, day=1)
            dame_bdate.replace(month=1, day=1)

        if child.bdate_mode == 2 or dame.bdate_mode == 2:
            child_bdate.replace(day=1)
            dame_bdate.replace(day=1)

        if child_bdate > dame_bdate:
            raise ValidationError("Дата рождения отца не может быть "
                                  "больше даты рождения лошади")


def validate_child(horse, child):
    if horse.sex == 0:
        validate_sire(child, horse)
    else:
        validate_dame(child, horse)


def validate_phone_numbers(phone_list):
    pattern = r'^(\+7|7|8)?\d{10}$'
    for phone in phone_list:
        if re.match(pattern, phone):
            continue
        else:
            raise ValidationError(f'{phone} не является номером телефона')
