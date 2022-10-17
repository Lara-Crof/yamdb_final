from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import validate_year


class Categories(models.Model):
    """Категория произведения (фильм, песня, книг и т.д.).
    Одна ко многим"""
    name = models.CharField(verbose_name='Категория', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категорий'

    def __str__(self):
        return self.slug


class Genres(models.Model):
    """Жанр произведения (комедия, фантистика, порно и т.д.).
    Много ко многим"""
    name = models.CharField(verbose_name='Жанр произведения', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Название и описание произведения.
    Базовая модель проекта"""
    name = models.CharField(
        verbose_name='Название произведения', max_length=256
    )
    year = models.PositiveSmallIntegerField(
        'ГОД', validators=(validate_year,),
        db_index=True
    )
    description = models.TextField(
        blank=True, verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(Genres, through='GenreTitle',
                                   verbose_name='Жанр')
    category = models.ForeignKey(
        Categories,
        verbose_name='Категория произведения',
        help_text='Категория, к которой относится произведение',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    """БД с жанрами и произведениями."""
    genry = models.ForeignKey(Genres, on_delete=models.CASCADE,
                              verbose_name='Жанр')
    titles = models.ForeignKey(Title, on_delete=models.CASCADE,
                               verbose_name='Произведения')

    def __str__(self):
        return f'{self.titles} {self.genry}'


class Review(models.Model):
    """Отзыв к произведению."""
    text = models.TextField(verbose_name='Текст Комментария')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения',
        validators=[MinValueValidator(0),
                    MaxValueValidator(10)])
    pub_date = models.DateField(verbose_name='Дата публикации',
                                auto_now_add=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведение')

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    """Коменнтарии к отзыву."""
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Отзыв')
    pub_date = models.DateField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
