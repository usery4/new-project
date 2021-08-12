import django_filters
from django.db.models import Count
from rest_framework import viewsets
from rest_framework import permissions, generics
from rest_framework import renderers
from main.models import Article
from .serializers import ArticleSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework import filters
from users.models import MyUser


class CountModelMixin(object):
    @action(detail=False)
    def count(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        result_list = list(queryset.values('username').annotate(count_of_articles=Count('articles')))
        return Response(result_list)


class CountModelMixins(object):
    @action(detail=False)
    def count(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        result_list = list(queryset.values('owner').annotate(count_of_articles=Count('title')))
        return Response(result_list)


class ArticleViewSet(viewsets.ModelViewSet, CountModelMixins):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['owner', ]
    search_fields = ['title', ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet, CountModelMixin):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes =[permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'username']
    search_fields = ['username']






class ArticleHighlight(generics.GenericAPIView):
    queryset = Article.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        return Response(article.highlighted)