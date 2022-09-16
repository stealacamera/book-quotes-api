from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ChangePasswordView, LogoutView, CurrentUserDisplay, ProfilesDisplay

router = DefaultRouter()
router.register('all', ProfilesDisplay, basename='profiles')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', CurrentUserDisplay.as_view(), name='current-profile'),
    path('', include(router.urls)),
]