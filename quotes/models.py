from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=70, unique=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    authors = models.ManyToManyField(Author, related_name='books')
    title = models.CharField(max_length=70, unique=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.title

class Category(models.Model):
    category = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name_plural = 'Categories'

class Quote(models.Model):
    quote = models.TextField()
    book = models.ForeignKey(Book, related_name='quotes', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='quotes')
    
    user = models.ForeignKey(User, related_name='user_quotes', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.quote