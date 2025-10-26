from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator

class KeyValueInformation(models.Model):
    name: models.CharField = models.CharField(
        verbose_name="Ключ информации для API",
        null=False,
        blank=False,
        unique=True,
        max_length=127,
        validators=[MaxLengthValidator(127)]
    )
    title: models.CharField = models.CharField(
        verbose_name="Человекочитаемое наименование",
        null=False,
        blank=False,
        max_length=255,
        validators=[MaxLengthValidator(255)]
    )
    value: models.CharField = models.CharField(
        verbose_name="Значение",
        null=False,
        blank=False
    )
    as_type: models.CharField = models.CharField(
        verbose_name="Тип данных",
        null=False,
        blank=False,
        max_length=31,
        validators=[MaxLengthValidator(31)]
    )

class ContactsGroups(models.Model):
    name: models.CharField = models.CharField(
        verbose_name="Наименование группы",
        max_length=127,
        null=False,
        blank=False,
        unique=True,
        validators=[MaxLengthValidator(127)]
    )

class Contacts(models.Model):
    main_title: models.CharField = models.CharField(
        verbose_name="Первичное наименование",
        null=False,
        blank=False,
        max_length=127,
        validators=[MaxLengthValidator(127)]
    )
    subtitle: models.CharField = models.CharField(
        verbose_name="Вторичное наименование",
        null=True,
        blank=True,
        max_length=127,
        validators=[MaxLengthValidator(127)]
    )
    phone_numbers: models.JSONField = models.JSONField(
        verbose_name="Номера телефонов",
        null=False,
        blank=False,
        default=list
    )
    group: models.ForeignKey = models.ForeignKey(
        to="static_information.ContactsGroups",
        verbose_name="Группа контактов",
        related_name="contacts",
        null=False,
        on_delete=models.CASCADE,
    )
    priority: models.IntegerField = models.IntegerField(
        verbose_name="Приоритет контакта",
        null=False,
        blank=False,
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(500)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "main_title"], name="unique_contact_group_main_title"
            )
        ]
