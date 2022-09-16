from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {'username': 'example',
                'email': 'example@example.com',
                'password': 'password',
                'password2': 'password'}
        
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogout(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example',
                                        email='example@example.com',
                                        password='password')
    
    def test_login(self):
        data = {'username': 'example',
                'password': 'password'}
        
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_logout(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProfileTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example1', password='password')
        User.objects.create_user(username='example2', password='password')
    
    def test_getall_retrieve_anon(self):
        response = self.client.get(reverse('profiles-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('profiles-detail', args=(self.user.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_getcurrent(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = self.client.get(reverse('current-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)