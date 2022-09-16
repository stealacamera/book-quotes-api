from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book, Quote, Category

class AuthorTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='example', password='password')        
        self.author = Author.objects.create(name='example')
    
    def test_getall_retrieve_anon(self):
        response = self.client.get(reverse('authors-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('authors-detail', args=(self.author.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_createupdatedelete_anon(self):
        data = {'name': 'example 2'}
        
        response = self.client.post(reverse('authors-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        data = {'name': 'changed'}
        
        response = self.client.put(reverse('authors-detail', args=(self.author.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.delete(reverse('authors-detail', args=(self.author.id,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_createupdatedelete_admin(self):
        token = Token.objects.get(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        data = {'name': 'example 2'}
        
        response = self.client.post(reverse('authors-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = {'name': 'changed'}
        
        response = self.client.put(reverse('authors-detail', args=(self.author.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.delete(reverse('authors-detail', args=(self.author.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class BookTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='example', password='password')
        
        self.author = Author.objects.create(name='example')        
        self.book = Book.objects.create(title='example')
        self.book.authors.set([self.author])
    
    def test_getall_retrieve_anon(self):
        response = self.client.get(reverse('books-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('books-detail', args=(self.book.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_createupdatedelete_anon(self):
        data = {'title': 'changed',
                'authors': self.author.id}
        
        response = self.client.post(reverse('books-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.put(reverse('books-detail', args=(self.book.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.delete(reverse('books-detail', args=(self.book.id,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_createupdatedelete_admin(self):
        token = Token.objects.get(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        data = {'title': 'example 2',
                'authors': self.author}
        
        response = self.client.post(reverse('books-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = {'title': 'changed',
                'authors': self.author}
        
        response = self.client.put(reverse('books-detail', args=(self.book.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.delete(reverse('books-detail', args=(self.book.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CategoryTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='example', password='password')
        self.category = Category.objects.create(category='example')
    
    def test_getall_retrieve_anon(self):
        response = self.client.get(reverse('categories-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('categories-detail', args=(self.category.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_createupdatedelete_anon(self):
        data = {'category': 'changed'}
        
        response = self.client.post(reverse('categories-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.put(reverse('categories-detail', args=(self.category.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.delete(reverse('categories-detail', args=(self.category.id,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_createupdatedelete_admin(self):
        token = Token.objects.get(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        data = {'category': 'example 2'}
        
        response = self.client.post(reverse('categories-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = {'category': 'changed'}
        
        response = self.client.put(reverse('categories-detail', args=(self.category.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.delete(reverse('categories-detail', args=(self.category.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class QuoteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example', password='password')
        self.admin = User.objects.create_superuser(username='example2', password='password')
        
        self.author = Author.objects.create(name='example')        
        self.book = Book.objects.create(title='example')
        self.book.authors.set([self.author])
        self.quote = Quote.objects.create(quote='example', book=self.book)
    
    def test_getall_retrieve_anon(self):
        response = self.client.get(reverse('quotes-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('quotes-detail', args=(self.quote.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_createupdatedelete_user(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        data = {'quote': 'changed',
                'book': self.book.id}
        
        response = self.client.post(reverse('quotes-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.put(reverse('quotes-detail', args=(self.quote.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.delete(reverse('quotes-detail', args=(self.quote.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_updatedelete_admin(self):
        token = Token.objects.get(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        data = {'quote': 'changed', 
                'book': self.book.id}
        
        response = self.client.put(reverse('quotes-detail', args=(self.quote.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.delete(reverse('quotes-detail', args=(self.quote.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_randomquote(self):
        response = self.client.get(reverse('random-quote'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        