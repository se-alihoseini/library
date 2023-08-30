from rest_framework import serializers


class EmailPhoneSerializer(serializers.Serializer):
    email_phone = serializers.CharField()


class OtpAuthSerializer(serializers.Serializer):
    email_phone = serializers.CharField()
    code = serializers.CharField()
