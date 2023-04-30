from rest_framework import serializers
from .models import UserProfile, CustomUser
from message_control.serializers import GenerivFileUploadSerializer
from django.db.models import Q


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ("password", )


class UserProfileSerializers(serializers.ModelSerializer):
    user = CustomUserSerializers(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    profile_picture = GenerivFileUploadSerializer(read_only=True)
    profile_picture_id = serializers.IntegerField(
        write_only=True, required=False)
    message_count = serializers.SerializerMethodField("get_message_count")

    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_message_count(self, obj):
        user_id = self.context["request"].user.id

        from message_control.models import Message
        message = Message.objects.filter(
            Q(sender_id=user_id, receiver_id=obj.user_id) | Q(sender_id=user_id, receiver_id=obj.user_id)).distinct()

        return message.count()
