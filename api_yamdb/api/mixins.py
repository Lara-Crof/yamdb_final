from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """Миксин для создания, удаления и получения списка объектов."""
    pass
