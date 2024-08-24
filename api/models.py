from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    gender = models.CharField(max_length=10, blank=True)
    image_url = models.URLField(blank=True)
    about = models.TextField(blank=True)
    fans_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', db_index=True)
    author_name = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=13)  # Убрали unique=True
    isbn13 = models.CharField(max_length=13, blank=True)
    asin = models.CharField(max_length=10, blank=True)
    language = models.CharField(max_length=3)
    average_rating = models.FloatField(default=0)
    ratings_count = models.IntegerField(default=0)
    text_reviews_count = models.IntegerField(default=0)
    publisher = models.CharField(max_length=200)
    num_pages = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=100, db_index=True)
    
    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
