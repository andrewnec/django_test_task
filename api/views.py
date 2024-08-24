from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q, F
from collections import Counter
from .models import Author, Book, Favorite
from .serializers import AuthorSerializer, BookSerializer, FavoriteSerializer, WriteFavoriteSerializer, ReadFavoriteSerializer
from .filters import BookFilter
from django.db import models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    
class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadFavoriteSerializer
        return WriteFavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.get_queryset().count() >= 20:
            return Response({"error": "Maximum favorites limit reached"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'], url_path='remove')
    def remove_favorite(self, request):
        book_id = request.data.get("book")
        if not book_id:
            return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        favorite = Favorite.objects.filter(user=self.request.user, book_id=book_id).first()
        if not favorite:
            return Response({"error": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND)

        favorite.delete()
        return Response({"success": "Favorite removed"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        favorites = self.get_queryset()
        if not favorites:
            return Response({"error": "No favorites found"}, status=status.HTTP_400_BAD_REQUEST)

        genres = Counter()
        authors = Counter()
        descriptions = []
        book_ids = []

        for favorite in favorites:
            genres[favorite.book.genre] += 1
            authors[favorite.book.author.id] += 1
            descriptions.append(favorite.book.description)
            book_ids.append(favorite.book.id)

        similar_books = Book.objects.exclude(id__in=favorites.values_list('book_id', flat=True))
        
        if descriptions:
            tfidf_vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions)
            cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        similar_books = similar_books.annotate(
            genre_similarity=Count('genre', filter=Q(genre__in=genres.keys())),
            author_similarity=Count('author', filter=Q(author_id__in=authors.keys()))
        )
        
        similar_books = similar_books.annotate(
            similarity=F('genre_similarity') * 0.4 + F('author_similarity') * 0.3 +
                        (cosine_similarities * 0.3 if descriptions else 0)
        ).order_by('-similarity')[:5]
        
        serializer = BookSerializer(similar_books, many=True)
        return Response(serializer.data)
