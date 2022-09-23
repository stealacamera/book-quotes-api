from rest_framework import serializers
from .models import Author, Book, Quote, Category

class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(read_only=True, many=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

class BookSerializer(serializers.ModelSerializer):
    quotes = serializers.StringRelatedField(read_only=True, many=True)
    authors = serializers.SlugRelatedField(queryset=Author.objects.all(), many=True, slug_field='name')
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'description', 'quotes']

class CategorySerializer(serializers.ModelSerializer):
    quotes = serializers.StringRelatedField(read_only=True, many=True)
    
    class Meta:
        model = Category
        fields = ['id', 'category', 'quotes']

class QuoteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    categories = serializers.SlugRelatedField(queryset=Category.objects.all(), many=True, slug_field='category')
    
    class Meta:
        model = Quote
        fields = '__all__'
        
    def to_representation(self, instance):
        rep = super(QuoteSerializer, self).to_representation(instance)
        rep['book'] = instance.book.title
        return rep