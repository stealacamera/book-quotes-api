from random import randint
from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from .models import Author, Book, Quote, Category
from .serializers import AuthorSerializer, BookSerializer, QuoteSerializer, CategorySerializer
from .permissions import QuotePermission, ContentPermission

class AuthorDisplay(ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer
    
    permission_classes = [ContentPermission]

class BookDisplay(ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer

    permission_classes = [ContentPermission]

class CategoryDisplay(ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    
    permission_classes = [ContentPermission]

class QuoteDisplay(ModelViewSet):
    queryset = Quote.objects.all().order_by('id')
    serializer_class = QuoteSerializer
    
    permission_classes = [QuotePermission]
    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['categories', 'book']
    search_fields = ['quote']

class RandomQouteList(ListAPIView):
    serializer_class = QuoteSerializer
    pagination_class = None
    
    def get_queryset(self):
        max_id = Quote.objects.aggregate(Max('id'))['id__max']
        random_pk = 0
        
        if not Quote.objects.filter(pk=random_pk).exists():
            random_pk = randint(1, max_id)
            
        return Quote.objects.filter(pk=random_pk)