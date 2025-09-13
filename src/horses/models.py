from django.core.cache import cache
from django.core.validators import (MaxLengthValidator,
                                    MaxValueValidator,
                                    MinLengthValidator,
                                    MinValueValidator)
from django.db import models
from django.db.models import Prefetch
from django.utils import timezone

from gallery.models import Photo

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

KIND_CHOICES = [
    (0, "Лошадь"),
    (1, "Пони"),
]

HORSE_OWNER_TYPE_CHOICES = [
    (0, "Юридическое лицо"),
    (1, "Физическое лицо"),
    (2, "Неизвестно"),
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
    kind = models.PositiveSmallIntegerField(verbose_name="Тип",
                                            null=False,
                                            blank=False,
                                            choices=KIND_CHOICES,
                                            default=0,
                                            validators=[MinValueValidator(0),
                                                        MaxValueValidator(1)])
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
                                    related_name='horses')
    owner = models.ForeignKey(to="horses.HorseOwner",
                              verbose_name="Владелец",
                              related_name='horses',
                              null=True,
                              on_delete=models.SET_NULL)
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

        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['sex']),
            models.Index(fields=['bdate']),
            models.Index(fields=['ddate']),
            models.Index(fields=['breed']),
        ]

    def __str__(self):
        return self.name

    def get_pedigree(self, count=3, serializer=None):
        def build_pedigree_tree(horse, current_depth, max_depth):
            if (horse is None or
                    serializer is None or
                    current_depth >= max_depth):
                return None

            horse_data = serializer(horse).data

            if current_depth + 1 != max_depth:
                sire = horse.get_sire(True)
                dame = horse.get_dame(True)

                horse_data['sire'] = build_pedigree_tree(
                    sire, current_depth + 1, max_depth
                )

                horse_data['dame'] = build_pedigree_tree(
                    dame, current_depth + 1, max_depth
                )

            return horse_data

        pedigree_data = {
            "sire": build_pedigree_tree(self.get_sire(), 0, count),
            "dame": build_pedigree_tree(self.get_dame(), 0, count),
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

    def get_sire(self, prefetch_parents=False):
        cache_key = f'horse_{self.id}_sire'
        sire = cache.get(cache_key)
        if sire:
            return sire

        if hasattr(self, 'prefetched_parents'):
            sire = list(filter(lambda parent: parent.sex == 0,
                               self.prefetched_parents))
            if sire:
                cache.set(cache_key, sire[0], timeout=60 * 15)
                return sire[0]
            return None

        photos_prefetch = Prefetch(
            'photos',
            queryset=Photo.objects.all(),
            to_attr='prefetched_photos'
        )

        prefetch = [photos_prefetch]

        if prefetch_parents:
            prefetch_parents = Prefetch(
                lookup="parents",
                queryset=Horse.objects.select_related(
                    'breed').prefetch_related('photos'),
                to_attr="prefetched_parents"
            )
            prefetch.append(prefetch_parents)

        sire = self.parents.filter(
            sex=0
        ).select_related('breed').prefetch_related(*prefetch).first()
        cache.set(cache_key, sire, timeout=60 * 15)
        return sire

    def get_dame(self, prefetch_parents=False):
        cache_key = f'horse_{self.id}_dame'
        dame = cache.get(cache_key)
        if dame:
            return dame

        if hasattr(self, 'prefetched_parents'):
            dame = list(filter(lambda parent: parent.sex in [1, 2],
                               self.prefetched_parents))
            if dame:
                cache.set(cache_key, dame[0], timeout=60 * 15)
                return dame[0]
            return None

        photos_prefetch = Prefetch(
            'photos',
            queryset=Photo.objects.all(),
            to_attr='prefetched_photos'
        )

        prefetch = [photos_prefetch]

        if prefetch_parents:
            prefetch_parents = Prefetch(
                lookup="parents",
                queryset=Horse.objects.select_related(
                    'breed').prefetch_related('photos'),
                to_attr="prefetched_parents"
            )
            prefetch.append(prefetch_parents)

        dame = self.parents.filter(
            sex__in=[1, 2]
        ).select_related('breed').prefetch_related(*prefetch).first()
        cache.set(cache_key, dame, timeout=60 * 15)
        return dame

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
    name = models.CharField(verbose_name="Наименование",
                            null=False,
                            blank=False,
                            max_length=50,
                            validators=[MinLengthValidator(5),
                                        MaxLengthValidator(50)])
    description = models.CharField(verbose_name="Описание",
                                   null=True,
                                   blank=True,
                                   max_length=500,
                                   validators=[MinLengthValidator(5),
                                               MaxLengthValidator(500)])

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'
        ordering = ['name']

    def __str__(self):
        return self.name


class HorseOwner(models.Model):
    name = models.CharField(verbose_name="Наименование",
                            null=False,
                            blank=False,
                            max_length=150,
                            validators=[MaxLengthValidator(150)])
    description = models.CharField(verbose_name="Описание",
                                   null=True,
                                   blank=True,
                                   max_length=500,
                                   validators=[MaxLengthValidator(500)])
    type = models.PositiveSmallIntegerField(verbose_name="Тип",
                                            null=False,
                                            blank=False,
                                            choices=HORSE_OWNER_TYPE_CHOICES,
                                            default=0,
                                            validators=[MinValueValidator(0),
                                                        MaxValueValidator(2)])
    address = models.CharField(verbose_name="Адрес",
                               null=True,
                               blank=True,
                               max_length=200,
                               validators=[MaxLengthValidator(200)])
    phone_number = models.JSONField(verbose_name="Номера телефонов",
                                    null=True,
                                    blank=True,
                                    default=list)
