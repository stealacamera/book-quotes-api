from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterSerializer, PasswordChangeSerializer, ProfileSerializer

class RegisterView(APIView):
    def post(self, request):
        serialized = RegisterSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        
        account = serialized.save()
        data = {'username': account.username,
                'email': account.email,
                'token': Token.objects.get(user=account).key
                }
        
        return Response(data, status=status.HTTP_201_CREATED)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serialized = PasswordChangeSerializer(data=request.data, context={'request': request})
        serialized.is_valid(raise_exception=True)
        serialized.save()
        
        return Response({'Password changed successfully!'}, status=status.HTTP_202_ACCEPTED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'Logged out successfully!'}, status=status.HTTP_200_OK)

class CurrentUserDisplay(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def get(self, request):
        serialized = ProfileSerializer(request.user)
        return Response(serialized.data, status=status.HTTP_200_OK)

class ProfilesDisplay(ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = ProfileSerializer