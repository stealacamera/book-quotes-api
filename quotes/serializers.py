from rest_framework import serializers
from .models import Author, Book, Quote, Category

#
# Related fields
# Outputs names, instead of ids
#

class AuthorsRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return Author.objects.get(name=data)

class CategoryRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return str(value)
    
    def to_internal_value(self, data):
        return Category.objects.get(category=data)

#
# Model serializers
#

class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(read_only=True, many=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

class BookSerializer(serializers.ModelSerializer):
    quotes = serializers.StringRelatedField(read_only=True, many=True)
    authors = AuthorsRelatedField(queryset=Author.objects.all(), many=True)
    
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
    categories = CategoryRelatedField(queryset=Category.objects.all(), many=True)
    
    class Meta:
        model = Quote
        fields = '__all__'
        
    def to_representation(self, instance):
        rep = super(QuoteSerializer, self).to_representation(instance)
        rep['book'] = instance.book.title
        return rep