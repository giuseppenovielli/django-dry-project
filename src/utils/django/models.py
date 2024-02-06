
from django.contrib import auth

def get_user_model():
    return auth.get_user_model()