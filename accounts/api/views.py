from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import PhoneSerializer, OtpCodeSerializer
from accounts.models import OtpCode, User
from datetime import datetime, timedelta
from products.utils import generate_text
from accounts.senders import SmsSender


class LoginViewSet(ViewSet):
    @action(detail=False, methods=['get'])
    def phone_login(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone']
            otp_code: str = generate_text(5)
            OtpCode.objects.create(
                phone=phone_number,
                otp_code=otp_code
            )

            try:
                SmsSender.send(otp_code, phone_number)
                return Response({"Message": f"Sms Send, otp-code:{otp_code}"})
            except:
                return Response({"Otp Code": otp_code})
        else:
            return Response({"Errors": serializer.errors})

    @action(detail=False, methods=['get'])
    def validate_phone(self, request):
        serializer = OtpCodeSerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            current_time = datetime.now()
            is_otp_code = OtpCode.objects.get(
                otp_code=otp_code,
                created__lt=current_time,
                created__gt=current_time - timedelta(seconds=120),
                is_valid=False
            )
            if is_otp_code:
                user = User.objects.get(phone=is_otp_code.phone)
                refresh = RefreshToken.for_user(user)
                access = str(refresh.access_token)
                is_otp_code.is_valid = True
                is_otp_code.save()
                return Response(
                    {
                        'refresh': str(refresh),
                        'access': access
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"Message": "OtpCode is not valid"}, status=status.HTTP_400_BAD_REQUEST)
