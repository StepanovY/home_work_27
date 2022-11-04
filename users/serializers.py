from rest_framework import serializers

from users.models import User, Location


class UserListSerializer(serializers.ModelSerializer):
    """
    сериализатор вывода списка всех и только одной по id
    """
    location = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    total_ads = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_total_ads(self, user):
        return user.ads.filter(is_published=True).count()


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('location', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(validated_data['password'])

        for location in self._location:
            loc, _ = Location.objects.get_or_create(name=location)
            user.location.add(loc)

        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'age', 'location']

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('location')
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()

        for location in self._location:
            loc, _ = Location.objects.get_or_create(name=location)
            user.location.add(loc)

        user.save()

        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
