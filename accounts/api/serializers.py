from datetime import datetime
from rest_framework import serializers


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)


class OtpCodeSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=5)