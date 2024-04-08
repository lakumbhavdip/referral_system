from django.urls import path
from .views import (
    UserRegistrationView,
    UserDetailView,
    ReferralListView,
)
urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='users-register'),
    path('details', UserDetailView.as_view(), name='users-details'),
    path('referral-list', ReferralListView.as_view(), name='referral-list'),
     
]