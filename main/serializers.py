from rest_framework import serializers
from .models import Article
from users.models import MyUser


class ArticleSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Article
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = MyUser
        fields = ['id', 'owner', 'username', 'articles', 'profile_pic']

