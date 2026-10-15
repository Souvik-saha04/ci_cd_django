from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
urlpatterns=[
    path('login/',Login),
    path("welcome/",Welcome),
    path('logout/',Logout),
    path('token/refresh/',TokenRefreshView.as_view()),
    
]