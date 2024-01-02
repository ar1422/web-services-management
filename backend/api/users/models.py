from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from uuid import uuid4
from helper import encode_token


class AuthUser(models.Model):

    class Meta:
        db_table: str = "api_auth_users"

    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    email = models.EmailField(max_length=255, db_index=True, null=False, blank=False, unique=True)
    username = models.CharField(max_length=50, db_index=True, null=False, blank=False, unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def set_password(self, user_password):
        self.password = make_password(user_password)

    def check_password(self, user_entry):
        return check_password(user_entry, self.password)

    def set_token(self, email: str) -> None:
        self.token = encode_token(email, settings.SECRET_KEY)