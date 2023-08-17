from rest_framework import serializers


class UserPassSerializer(serializers.Serializer):
    email_phone = serializers.CharField()
    password = serializers.CharField()


class OtpAuthSerializer(serializers.Serializer):
    email_phone = serializers.CharField()
    password = serializers.CharField()
    code = serializers.IntegerField()

class GeneratePasswordSerializer(serializers.Serializer):
    email_phone = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError()
        return data
