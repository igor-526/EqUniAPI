from django.contrib.auth.models import AbstractUser
from django.db import models


class NewUser(AbstractUser):
    patronymic = models.CharField(verbose_name="Отчество",
                                  null=True,
                                  blank=True,
                                  max_length=50)
    photo = models.ImageField(verbose_name='Фотография профиля',
                              upload_to='profile_pictures/',
                              null=False,
                              blank=True,
                              default='profile_photos/base_avatar.png')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-is_active', 'last_name', 'first_name', 'patronymic']

    def __str__(self):
        full_name = f'{self.last_name} {self.first_name}'
        if self.patronymic:
            full_name += f' {self.patronymic}'
        return full_name
