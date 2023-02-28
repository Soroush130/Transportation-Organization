from kavenegar import *
from Transport.settings import KAVENEGARAPI


class SmsSender:
    def __init__(self):
        pass

    @classmethod
    def send(cls, code: str, phone: str):
        api = KavenegarAPI(KAVENEGARAPI)
        message = f"Otp-Code: {code}"
        params = {
            'sender': '10008663',
            'receptor': phone,
            'message': message
        }
        response = api.sms_send(params)
        return response
