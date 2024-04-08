from django.contrib.auth import login, logout
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .permissions import IsNotAuthenticated
from .serializers import UserLoginSerializer, UserSerializer


class LoginAPIView(GenericAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'message': 'Вход выполнен', 'token': token.key}, status=status.HTTP_200_OK)
        return JsonResponse({'detail': 'Неверные данные'}, status=status.HTTP_400_BAD_REQUEST)


class SignUpAPIView(GenericAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = UserSerializer

    def post(self, request):
        self.check_permissions(request)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Пользователь создан'}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        logout(request)
        return JsonResponse({'message': 'Выход выполнен'}, status=200)
