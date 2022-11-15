from rest_framework import serializers

from ads.models import Ad
from ads.serializers import AdListSerializer
from selection.models import Selection
from users.models import User


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDetailSerializer(serializers.ModelSerializer):
    ads = AdListSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    ad = serializers.SlugRelatedField(
        required=False,
        queryset=Ad.objects.all(),
        slug_field='id'
    )
    author = serializers.SlugRelatedField(
        required=False,
        queryset=User.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    ad = serializers.SlugRelatedField(
        required=False,
        queryset=Ad.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id']
