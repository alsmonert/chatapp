from rest_framework import serializers
from .models import GenericFileUpload, Message, MessageAttachment


class GenerivFileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenericFileUpload
        fields = "__all__"


class MessageAttachmentSerializer(serializers.ModelSerializer):
    attachment = GenerivFileUploadSerializer()

    class Meta:
        models = MessageAttachment
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField("get_user_data")
    sender = serializers.SerializerMethodField("get_sender_data")
    sender_id = serializers.IntegerField(write_only=True)
    receiver = serializers.SerializerMethodField("get_receiver_data")
    receiver_id = serializers.IntegerField(write_only=True)
    message_attachments = MessageAttachmentSerializer(
        read_only=True, many=True)

    class Meta:
        models = Message
        fields = "__all__"

    def get_user_data(self, obj):
        from user_control.serializers import UserProfileSerializers
        return UserProfileSerializers(obj.sender.user_profile).data
