from django.contrib.auth import get_user_model
from rest_framework import serializers
from main.models import Status

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ("id", "username", "password", "first_name", "last_name", "email")


class StatusSerializer(serializers.Serializer):
    """
    Сериализатор преобразует статусы (объекты моделей) в список Python,
    который мы может вернуть в API-запросе
    """
    status = serializers.CharField(max_length=200)
    user_id = serializers.IntegerField()

    def create(self, validated_data):
        """
        Метод сообщит сериализатору, что делать, когда вызывается метод save сериализатора
        """
        return Status.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Метод обновляет статус
        В том случае если мы что-то передаем в экземпляр статуса, который мы хотим обновить,
        мы переназначаем это значение, в противном случае мы сохраняем старое значение атрибута.
        """
        instance.status = validated_data.get('status', instance.status)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.save()
        return instance



class DialogSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    create_date = serializers.DateTimeField()
    last_change = serializers.DateTimeField()
    # users = serializers.

