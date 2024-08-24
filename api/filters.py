import django_filters
from django.db import models 
from .models import Book

class BookFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label="Search")

    class Meta:
        model = Book
        fields = ['search']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) | 
            models.Q(author__name__icontains=value)
        )
