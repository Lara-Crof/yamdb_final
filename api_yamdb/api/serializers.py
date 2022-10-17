from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Categories, Comment, Genres, Review, Title
from users.models import User
from users.validators import usernamevalidator


class ErrorResponse:
    """Класс ошибок для сериализатора произведений."""
    INCORRECT_RELEASE_YEAR = 'Год не может быть больше текущего'
    INCORRECT_GENRE = 'Жанр не входит в представленный список'
    INCORRECT_CATEGORY = 'Категория не входит в представленный список'


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор Категорий."""
    class Meta:
        fields = ('name', 'slug')
        model = Categories
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CategoriesField(serializers.SlugRelatedField):
    """Сериализатор для поиска по катергорий."""
    def to_representation(self, value):
        serializer = CategoriesSerializer(value)
        return serializer.data


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор Жанра."""

    class Meta:
        fields = ('name', 'slug')
        model = Genres
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenresField(serializers.SlugRelatedField):
    """Сериализатор для поиска по Жанру."""
    def to_representation(self, value):
        serializer = GenresSerializer(value)
        return serializer.data


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
    category = CategoriesField(
        slug_field='slug', queryset=Categories.objects.all()
    )
    genre = GenresField(
        slug_field='slug', queryset=Genres.objects.all(), many=True
    )
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        """Валидация года произведения."""
        year = timezone.now().year
        if year < value:
            raise serializers.ValidationError(
                ErrorResponse.INCORRECT_RELEASE_YEAR
            )
        return value

    def validate_genre(self, value):
        """Проверка жанра на существование."""
        genre = Genres.objects.all()
        for item in value:
            if item not in genre:
                raise serializers.ValidationError(
                    ErrorResponse.INCORRECT_GENRE
                )
        return value

    def validate_category(self, value):
        """Проверка категорий на существование."""
        category = Categories.objects.all()
        if value not in category:
            raise serializers.ValidationError(
                ErrorResponse.INCORRECT_CATEGORY)
        return value


class ReadTitleSerializer(serializers.ModelSerializer):
    """Сериализатор предназначеный для чтения клиентами."""
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов к произведениям."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        """Проверка на то, что автор не может,
        написать два отзыва к оджному произведению."""
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError('Отзыв уже существует!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатора Комметариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор Пользователя."""
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ])

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, username):
        """Проверка никнейма пользователя.
        Оно не должно быть me."""
        usernamevalidator(username)
        return username


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'confirmation_code',
            'username'
        )
        extra_kwargs = {
            'username': {
                'validators': [
                    UniqueValidator(queryset=User.objects.all())
                ]
            }
        }
