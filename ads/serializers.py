from rest_framework import serializers

from ads.models import Ad, Category
from ads.validators import not_published
from users.models import User


class AdListSerializer(serializers.ModelSerializer):
    """
    сериализатор вывода списка всех и только одной по id
    """
    author = serializers.SlugRelatedField(read_only=True, slug_field='first_name')
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    is_published = serializers.BooleanField(validators=[not_published])
    author = serializers.SlugRelatedField(
        required=False,
        queryset=User.objects.all(),
        slug_field='id'
    )
    category = serializers.SlugRelatedField(
        required=False,
        queryset=Category.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = Ad
        fields = '__all__'


class AdUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    author = serializers.SlugRelatedField(
        required=False,
        queryset=User.objects.all(),
        slug_field='id'
    )
    category = serializers.SlugRelatedField(
        required=False,
        queryset=Category.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = Ad
        fields = ['id', 'name', 'price', 'author', 'description', 'is_published', 'category']


class AdDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'
