from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ApiSingUp, CategoriesViewSet, CommentViewSet,
                    GenresViewSet, ReviewViewSet, TitlesViewSet, TokenView,
                    UserViewSet)

router_v1 = DefaultRouter()
router_v1.register('categories', CategoriesViewSet, basename='category')
router_v1.register('genres', GenresViewSet, basename='genre')
router_v1.register('titles', TitlesViewSet, basename='title')
router_v1.register('users', UserViewSet, basename='user')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='title_reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='reviews_comments')

auth_token_path = [path('auth/signup/', ApiSingUp.as_view()),
                   path('auth/token/', TokenView.as_view()),
                   ]


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(auth_token_path))
]
