from django.urls import path, include
from .views import ArticleViewSet, UserViewSet
from rest_framework.routers import DefaultRouter
from main import views


router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='article')
router.register('users', UserViewSet, basename='user')


urlpatterns = [

    path('', include(router.urls)),


]