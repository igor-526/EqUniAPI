from django.core.validators import (MaxLengthValidator,
                                    MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from django.utils import timezone

from .validators import validate_future_date

SEX_CHOICES = [
    (0, "Кобыла"),
    (1, "Жеребец"),
    (2, "Мерин"),
]

DATE_MODE_CHOICES = [
    (0, "Полная дата"),
    (1, "Только год"),
    (2, "Год и месяц"),
]


class Horse(models.Model):
    name = models.CharField(verbose_name="Кличка",
                            null=False,
                            blank=False,
                            max_length=50,
                            validators=[MaxLengthValidator(50)])
    breed = models.ForeignKey(to="horses.Breed",
                              verbose_name="Порода",
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL)
    sex = models.PositiveSmallIntegerField(verbose_name="Пол",
                                           null=False,
                                           blank=False,
                                           choices=SEX_CHOICES,
                                           default=0,
                                           validators=[MinValueValidator(0),
                                                       MaxValueValidator(2)])
    bdate = models.DateField(verbose_name="Дата рождения",
                             null=True,
                             blank=True,
                             validators=[validate_future_date])
    bdate_mode = models.PositiveSmallIntegerField(
        verbose_name="Тип даты рождения",
        null=False,
        blank=False,
        choices=DATE_MODE_CHOICES,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(2)]
    )
    ddate = models.DateField(verbose_name="Дата смерти",
                             null=True,
                             blank=True,
                             validators=[validate_future_date])
    ddate_mode = models.PositiveSmallIntegerField(
        verbose_name="Тип даты смерти",
        null=False,
        blank=False,
        choices=DATE_MODE_CHOICES,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(2)]
    )
    description = models.CharField(verbose_name="Описание",
                                   null=True,
                                   blank=True,
                                   max_length=500,
                                   validators=[MaxLengthValidator(500)])
    children = models.ManyToManyField(to="horses.Horse",
                                      verbose_name="Дети",
                                      related_name='parents')
    photos = models.ManyToManyField(to="gallery.Photo",
                                    verbose_name="Фотографии",
                                    related_name='horse')
    created_at = models.DateTimeField(
        verbose_name="Дата и время добавления лошади",
        auto_now_add=True,
        null=False,
        validators=[validate_future_date]
    )
    created_by = models.ForeignKey(to="profile_management.NewUser",
                                   verbose_name="Создатель",
                                   null=True,
                                   blank=True,
                                   related_name="horses_created",
                                   on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Лошадь'
        verbose_name_plural = 'Лошади'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_pedigree(self, count=3, serializer=None):
        def build_pedigree_tree(horse, current_depth, max_depth):
            if (horse is None or
                    serializer is None or
                    current_depth >= max_depth):
                return None

            horse_data = serializer(horse).data

            mother = horse.mother
            father = horse.father

            horse_data['mother'] = build_pedigree_tree(
                mother, current_depth + 1, max_depth
            )
            horse_data['father'] = build_pedigree_tree(
                father, current_depth + 1, max_depth
            )

            return horse_data

        pedigree_data = {
            "mother": build_pedigree_tree(self.mother, 0, count),
            "father": build_pedigree_tree(self.father, 0, count),
        }
        return pedigree_data

    def set_breed(self, breed: str):
        if breed == "none":
            self.breed = None
            self.save()
            return None
        try:
            breed_id = int(breed)
            breed = Breed.objects.get(id=breed_id)
        except ValueError:
            breed = Breed.objects.get_or_create(name=breed)[0]
        except Breed.DoesNotExist:
            breed = None
        self.breed = breed
        self.save()
        return None

    def set_photos(self, photos: list[int] | None = None,
                   mode: str = "add") -> None:
        if photos is None:
            return None
        if mode == "remove":
            self.photos.filter(id__in=photos).delete()
            return None
        if mode == "replace":
            self.photos.all().delete()
        self.photos.add(*photos)
        return None

    @staticmethod
    def _get_strformat(mode: int) -> str:
        if mode == DATE_MODE_CHOICES[1][0]:
            return '%m.%Y'
        elif mode == DATE_MODE_CHOICES[2][0]:
            return '%Y'
        return '%d.%m.%Y'

    @property
    def mother(self):
        return self.parents.filter(sex=0).first()

    @property
    def father(self):
        return self.parents.filter(sex__in=[1, 2]).first()

    @property
    def age(self):
        if not self.bdate:
            return None
        last_date = self.ddate if self.ddate else timezone.now().date()
        return int((last_date - self.bdate).days // 365.2425)

    @property
    def bdate_formatted(self):
        if not self.bdate:
            return None
        return self.bdate.strftime(self._get_strformat(self.bdate_mode))

    @property
    def ddate_formatted(self):
        if not self.ddate:
            return None
        return self.ddate.strftime(self._get_strformat(self.ddate_mode))


class Breed(models.Model):
    name = models.CharField(verbose_name="Кличка",
                            null=False,
                            blank=False,
                            max_length=50,
                            validators=[MinValueValidator(5),
                                        MaxLengthValidator(50)])
    description = models.CharField(verbose_name="Описание",
                                   null=True,
                                   blank=True,
                                   max_length=500,
                                   validators=[MinValueValidator(3),
                                               MaxLengthValidator(500)])

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'
        ordering = ['name']

    def __str__(self):
        return self.name
