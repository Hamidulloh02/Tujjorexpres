# utils.py
from jwt import encode, decode, exceptions
import datetime

from rest_framework_simplejwt.tokens import AccessToken

# Xususiy kalitni o'qish
with open("private.pem", "r") as f:
    private_key = f.read()

# Ommaviy kalitni o'qish
with open("public.pem", "r") as f:
    public_key = f.read()

def create_jwt_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow()
    }
    token = encode(payload, private_key, algorithm="RS256")
    return token

def verify_jwt_token(token):
    try:
        decoded = decode(token, public_key, algorithms=["RS256"])
        return decoded
    except exceptions.ExpiredSignatureError:
        print("Token muddati o'tib ketgan!")
    except exceptions.InvalidTokenError:
        print("Yaroqsiz token!")


class CustomAccessToken(AccessToken):
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        self.payload["sub"] = "ex-tujjorexpress"  # O'z tizimingiz nomini kiriting
