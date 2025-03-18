from rest_framework_simplejwt.tokens import AccessToken

class CustomAccessToken(AccessToken):
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        self.payload["sub"] = "ex-tujjorexpress"  # O'z tizimingiz nomini kiriting