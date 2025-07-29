from django.core.validators import (MaxLengthValidator,
                                    MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from django.db.models import Count, QuerySet
from django.http import QueryDict
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

    @staticmethod
    def get_queryset(query_params: QueryDict, queryset=None) -> QuerySet:
        name = query_params.get('name')
        sex = query_params.getlist('sex')
        bdate_year_start = query_params.get('bdate_year_start')
        bdate_year_end = query_params.get('bdate_year_end')
        ddate_year_start = query_params.get('ddate_year_start')
        ddate_year_end = query_params.get('ddate_year_end')
        breeds = query_params.getlist('breed')
        description = query_params.get('description')
        limit = query_params.get('limit')
        offset = query_params.get('offset')
        has_photo = query_params.get('has_photo')
        children_count = query_params.get('children_count')
        sort_params = query_params.getlist('sort')
        query_dict = dict()
        sort_list = list()
        if bdate_year_start:
            try:
                bdys = int(bdate_year_start)
                if bdys > 0:
                    query_dict['bdate__year__gte'] = bdys
            except ValueError:
                pass
        if bdate_year_end:
            try:
                bdye = int(bdate_year_end)
                if bdye > 0:
                    query_dict['bdate__year__lte'] = bdye
            except ValueError:
                pass

        if ddate_year_start:
            try:
                ddys = int(ddate_year_start)
                if ddys > 0:
                    query_dict['ddate__year__gte'] = ddys
            except ValueError:
                pass

        if ddate_year_end:
            try:
                ddye = int(ddate_year_end)
                if ddye > 0:
                    query_dict['bdate__year__lte'] = ddye
            except ValueError:
                pass

        if name is not None:
            query_dict['name__icontains'] = name
        if sex:
            query_dict['sex__in'] = sex
        if breeds:
            breeds_ids = []
            breeds_names = []
            for breed in breeds:
                try:
                    breeds_ids.append(int(breed))
                except ValueError:
                    breeds_names.append(breed)
            if breeds_ids:
                query_dict['breed__id__in'] = breeds_ids
            else:
                query_dict['breed__name__in'] = breeds_names
        if description:
            query_dict['description__icontains'] = description
        if has_photo == "true":
            query_dict['photos_c__gte'] = 1
        elif has_photo == "false":
            query_dict['photos_c'] = 0
        if children_count:
            try:
                cc = int(children_count)
                if cc == -1:
                    query_dict['children_c__gte'] = 1
                if cc >= 0:
                    query_dict['children_c'] = cc
            except ValueError:
                pass
        if limit is not None:
            try:
                limit = int(limit)
                if limit < 1 or limit > 50:
                    limit = 50
            except ValueError:
                limit = 50
        else:
            limit = 50
        if offset is not None:
            try:
                offset = int(offset)
                if offset < 0:
                    offset = 0
            except ValueError:
                offset = 0
        else:
            offset = 0
        if sort_params:
            for param in sort_params:
                if param == "breed":
                    sort_list.append("breed__name")
                elif param == "-breed":
                    sort_list.append("-breed__name")
                elif param in ["name", "-name", "sex", "-sex",
                               "bdate", "-bdate", "ddate", "-ddate",
                               "created_at", "-created_at"]:
                    sort_list.append(param)

        objects = queryset if queryset else Horse

        return objects.objects.annotate(
            children_c=Count("children"),
            photos_c=Count("photos")
        ).filter(**query_dict).order_by(
            *sort_list
        )[offset:offset+limit]

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
