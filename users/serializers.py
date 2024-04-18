from typing import Dict, Any
import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer as JwtTokenRefreshSerializer
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer as JwtTokenBlacklistSerializer
from rest_framework_simplejwt.settings import api_settings





