from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorDisplay, BookDisplay, QuoteDisplay, CategoryDisplay, RandomQouteList

router = DefaultRouter()
router.register('authors', AuthorDisplay, basename='authors')
router.register('books', BookDisplay, basename='books')
router.register('categories', CategoryDisplay, basename='categories')
router.register('', QuoteDisplay, basename='quotes')

urlpatterns = [
    path('random-quote/', RandomQouteList.as_view(), name='random-quote'),
    path('', include(router.urls))
]