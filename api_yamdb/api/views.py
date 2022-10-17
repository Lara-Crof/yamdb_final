from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Categories, Genres, Review, Title
from users.models import User

from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import AuthorModeratorAdminOrReadOnly, IsAdmin
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReadTitleSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitlesSerializer, TokenSerializer,
                          UserEditSerializer, UserSerializer)


class CategoriesViewSet(ListCreateDestroyViewSet):
    """Представление Категорий."""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        """Метод вызова разрешения, в зависимости от запроса."""
        if self.action == 'list':
            return (permissions.AllowAny(),)
        return (IsAdmin(),)


class GenresViewSet(ListCreateDestroyViewSet):
    """Представление Жанров."""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        """Метод вызова разрешения, в зависимости от запроса."""
        if self.action == 'list':
            return (permissions.AllowAny(),)
        return (IsAdmin(),)


class TitlesViewSet(viewsets.ModelViewSet):
    """Представление Произведений."""
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_permissions(self):
        """Метод вызова разрешения, в зависимости от запроса."""
        if self.action == 'list' or self.action == 'retrieve':
            return (permissions.AllowAny(),)
        return (IsAdmin(),)

    def get_serializer_class(self):
        """Метод вызова сериализатора, в зависимости от запроса."""
        if self.action in ('retrieve', 'list'):
            return ReadTitleSerializer
        return TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление Отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorAdminOrReadOnly,)

    def get_title_or_404(self):
        """Получение объекта произведения."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Получение списка или объекта отзывов к произведению"""
        title = self.get_title_or_404()
        return title.reviews.all()

    def perform_create(self, serializer):
        """Создание отзыва к произведению"""
        serializer.save(author=self.request.user,
                        title=self.get_title_or_404()
                        )


class CommentViewSet(viewsets.ModelViewSet):
    """Представление Комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorAdminOrReadOnly,)

    def get_review_or_404(self):
        """Получение объекта отзыва."""
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Получение комметариев к отзыву."""
        review = self.get_review_or_404()
        return review.comments.all()

    def perform_create(self, serializer):
        """Создание комментария к отзыву."""
        serializer.save(author=self.request.user,
                        review=self.get_review_or_404())


class UserViewSet(viewsets.ModelViewSet):
    """Представление пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    filter_fields = ('username',)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['GET', 'PATCH'],
            detail=False,
            serializer_class=UserEditSerializer,
            permission_classes=[permissions.IsAuthenticated],
            url_path='me')
    def user_self_profile(self, request):
        """Отдельный путь для получения странички с профилем пользователя."""
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ApiSingUp(APIView):
    """Регистрация нового пользователя."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """К url можно делать только POST запроосы.
        Для получения confirmation_code."""
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        confirmation_code = default_token_generator.make_token(user)
        user.email_user('Your code', confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    """Представление для получения токена."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """К url можно делать только POST запроосы.
        Для получения tokena."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        if default_token_generator.check_token(
                user,
                serializer.validated_data['confirmation_code']):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
