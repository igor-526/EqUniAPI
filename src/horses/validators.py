from datetime import date

from django.core.exceptions import ValidationError


def validate_future_date(value):
    if value > date.today():
        raise ValidationError("Дата не может быть в будущем")


def validate_mother(child, mother):
    if child == mother:
        raise ValidationError("Мать и ребёнок не могут совпадать")
    if mother.sex != 0:
        raise ValidationError("Мать не может быть жеребцом или мерином")

    selected_mother = child.parents.filter(sex=0).first()
    if selected_mother:
        raise ValidationError(f"Мать {child}: {selected_mother}")

    if child.bdate and mother.bdate:
        child_bdate = child.bdate
        mother_bdate = mother.bdate

        if child.bdate_mode == 1 or mother.bdate_mode == 1:
            child_bdate.replace(month=1, day=1)
            mother_bdate.replace(month=1, day=1)

        if child.bdate_mode == 2 or mother.bdate_mode == 2:
            child_bdate.replace(day=1)
            mother_bdate.replace(day=1)

        if child_bdate > mother_bdate:
            raise ValidationError("Дата рождения матери не может быть "
                                  "больше даты рождения лошади")

        if mother.ddate:
            mother_ddate = mother.ddate
            child_bdate = child.bdate

            if child.bdate_mode == 1 or mother.ddate_mode == 1:
                child_bdate.replace(month=1, day=1)
                mother_ddate.replace(month=1, day=1)

            if child.bdate_mode == 2 or mother.ddate_mode == 2:
                child_bdate.replace(day=1)
                mother_ddate.replace(day=1)

            if mother_ddate < child_bdate:
                raise ValidationError("Дата смерти матери не может быть "
                                      "раньше даты рождения лошади")


def validate_father(child, father):
    if child == father:
        raise ValidationError("Мать и отец не могут совпадать")

    if father.sex == 0:
        raise ValidationError("Отец не может быть кобылой")

    selected_father = child.parents.filter(sex__in=[1, 2]).first()
    if selected_father:
        raise ValidationError(f"Отец {child}: {selected_father}")

    if child.bdate and father.bdate:
        child_bdate = child.bdate
        father_bdate = father.bdate

        if child.bdate_mode == 1 or father.bdate_mode == 1:
            child_bdate.replace(month=1, day=1)
            father_bdate.replace(month=1, day=1)

        if child.bdate_mode == 2 or father.bdate_mode == 2:
            child_bdate.replace(day=1)
            father_bdate.replace(day=1)

        if child_bdate > father_bdate:
            raise ValidationError("Дата рождения отца не может быть "
                                  "больше даты рождения лошади")


def validate_child(horse, child):
    if horse.sex == 0:
        validate_mother(child, horse)
    else:
        validate_father(child, horse)
