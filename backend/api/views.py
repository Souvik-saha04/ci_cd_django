from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Welcome(request):
    return Response({"message":f"Welcome {request.user.username}"},status=status.HTTP_200_OK)


@api_view(['POST'])
def Login(request):
    username=request.data.get('username')
    password=request.data.get('password')
    if not username or not password :
        return Response({"message":"Username and password is not needed"})
    user=authenticate(username=username,password=password)
    if  user is None:
        return Response({"message":"Invlaid Credentials"},status=status.HTTP_401_UNAUTHORIZED)
    refresh=RefreshToken.for_user(user)
    access=refresh.access_token
    return Response({"refresh":str(refresh),"access":str(access)},status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Logout(request):
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response(
            {'error': 'Refresh token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {'message': 'You are successfully logged out !!'},
            status=status.HTTP_200_OK
        )
    except TokenError:
        return Response(
            {'error': 'Invalid or expired refresh token'},
            status=status.HTTP_400_BAD_REQUEST
        )