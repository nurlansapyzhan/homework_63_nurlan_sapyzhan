from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from accounts.managers import UserManager

GENDERS = (('male', 'Мужской'), ('female', 'Женский'), ('other', 'Другое'))


def validate_digits(value):
    if not value.isdigit():
        raise ValidationError('Phone number should contain only digits')


class Account(AbstractUser):
    email = models.EmailField(verbose_name='Электронная почта', unique=True, blank=True)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='avatars',
        verbose_name='Аватар',
        default='avatars/no_image.png'
    )
    user_info = models.TextField(
        max_length=512,
        null=True,
        verbose_name='Информация о пользователе'
    )
    phone_number = models.CharField(
        max_length=11,
        verbose_name='Номер телефона',
        unique=True,
        null=True,
        validators=[MinLengthValidator(11), validate_digits],
    )
    gender = models.CharField(
        choices=GENDERS,
        max_length=20,
        null=True,
        verbose_name='Пол'
    )
    liked_posts = models.ManyToManyField(
        verbose_name='Понравившиеся публикации',
        to='posts.Post',
        related_name='user_likes')
    subscriptions = models.ManyToManyField(
        verbose_name='Подписки',
        to='accounts.Account',
        related_name='subscribers')
    commented_posts = models.ManyToManyField(
        verbose_name='Прокомментированные публикации',
        to='posts.Post',
        related_name='user_comments'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UserManager()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
