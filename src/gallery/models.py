from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MaxLengthValidator
from django.db import models

from rest_framework.request import Request


class Photo(models.Model):
    title = models.CharField(verbose_name="Наименование",
                             max_length=100,
                             null=False,
                             blank=False,
                             validators=[MaxLengthValidator(100)])
    description = models.CharField(verbose_name="Описание",
                                   max_length=500,
                                   null=True,
                                   blank=True,
                                   validators=[MaxLengthValidator(500)])
    image = models.ImageField(verbose_name='Фотография',
                              upload_to='photos/',
                              null=False,
                              blank=False)
    category = models.ManyToManyField(to="gallery.PhotoCategory",
                                      verbose_name="Категория",
                                      related_name="photos")
    created_at = models.DateTimeField(
        verbose_name="Дата и время добавления фотографии",
        auto_now_add=True,
        null=False
    )
    created_by = models.ForeignKey(to="profile_management.NewUser",
                                   verbose_name="Создатель",
                                   null=True,
                                   blank=True,
                                   related_name="gallery_created",
                                   on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['-created_at']

    def __str__(self):
        return f'Изображение {self.title}'

    def set_categories(self, categories: list[str], replace=False):
        if categories[0] == "none":
            self.category.all().delete()
            self.save()
            return self
        new_categories = []
        for category in categories:
            try:
                category_id = int(category)
                new_categories.append(
                    PhotoCategory.objects.get(id=category_id)
                )
            except ValueError:
                new_categories.append(
                    PhotoCategory.objects.get_or_create(name=category)[0]
                )
            except PhotoCategory.DoesNotExist:
                continue
        if replace:
            self.category.all().delete()
        self.category.add(*[cat.id for cat in new_categories])
        self.save()
        return self

    @staticmethod
    def get_photos(request: Request, description: str = None,
                   categories: list[str | int] = None, key: str = "photos[]"):
        photos = request.data.getlist(key)
        result = []
        for photo in photos:
            if isinstance(photo, InMemoryUploadedFile):
                ph = Photo.objects.create(title=photo,
                                          description=description,
                                          image=photo,
                                          created_by=request.user)
                if categories:
                    ph.set_categories(categories)
                result.append(ph.id)
        photos = [photo for photo in photos if
                  isinstance(photo, str) or isinstance(photo, int)]
        result.extend(list(
            Photo.objects.filter(id__in=photos).values_list("id", flat=True)
        ))
        return result


class PhotoCategory(models.Model):
    name = models.CharField(verbose_name="Наименование",
                            max_length=100,
                            null=False,
                            blank=False,
                            validators=[MaxLengthValidator(100)])

    class Meta:
        verbose_name = 'Категория изображений'
        verbose_name_plural = 'Категории изображений'
        ordering = ['name']

    def __str__(self):
        return f'Категория {self.name}'
