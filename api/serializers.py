from rest_framework import serializers

from game.models import Game, FavoriteGame
from user.models import User


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('pk', 'name', 'price', 'url',)


class FavoriteGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteGame
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
