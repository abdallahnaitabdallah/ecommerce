from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'first_name', 'last_name', 'email','password')