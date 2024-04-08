from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import User, Referral
from .serializers import UserSerializer, ReferralSerializer
from django.contrib.auth import login

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            referred_by_code = request.data.get('referral_code')
            if referred_by_code:
                try:
                    referred_by = User.objects.get(referral_code=referred_by_code)
                    Referral.objects.create(user=user, referred_by=referred_by)
                    token, _ = Token.objects.get_or_create(user=user)  # Generate or retrieve the token for the user

                except User.DoesNotExist:
                    pass
            login(request, user)
            return Response({'user_id': user.id, 'message': 'Registration successful', 'token': token.key,}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class ReferralListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReferralSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Referral.objects.filter(referred_by=user).order_by('-registration_timestamp')
