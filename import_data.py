import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")
django.setup()

from api.models import Author, Book

def import_authors(num_rows=None):
    print(f"Importing authors --- (Limit: {num_rows} rows)")

    total_rows = 0
    for chunk in pd.read_json('./authors_trimmed.json', lines=True, chunksize=1000):
        for _, author_data in chunk.iterrows():
            Author.objects.update_or_create(
                id=author_data.get('id'),
                defaults={
                    'name': author_data.get('name', ''),
                    'gender': author_data.get('gender', ''),
                    'image_url': author_data.get('image_url', ''),
                    'about': author_data.get('about', ''),
                    'fans_count': author_data.get('fans_count', 0)
                }
            )
            total_rows += 1
            if num_rows and total_rows >= num_rows:
                print("Reached limit for authors import.")
                return
    print("Authors imported successfully.")

def import_books(num_rows=None):
    print(f"Importing books --- (Limit: {num_rows} rows)")
    total_rows = 0
    for chunk in pd.read_json('./books_trimmed.json', lines=True, chunksize=1000):
        for _, book_data in chunk.iterrows():
            author_id = book_data.get('author_id')
            author_name = book_data.get('author_name')

            author, created = Author.objects.get_or_create(
                id=author_id,
                defaults={'name': author_name}
            )
            Book.objects.create(
                id=book_data.get('id'),
                title=book_data.get('title', ''),
                author=author,
                author_name=author.name,
                isbn=book_data.get('isbn', ''),
                isbn13=book_data.get('isbn13', ''),
                language=book_data.get('language', ''),
                average_rating=book_data.get('average_rating', 0.0),
                ratings_count=book_data.get('ratings_count', 0),
                text_reviews_count=book_data.get('text_reviews_count', 0),
                publisher=book_data.get('publisher', ''),
                num_pages=int(book_data.get('num_pages', 0) or 0),
                description=book_data.get('description', '')
            )
            total_rows += 1
            if num_rows and total_rows >= num_rows:
                print("Reached limit for books import.")
                return
    print("Books imported successfully.")
if __name__ == "__main__":
    import_authors(num_rows=2000)
    import_books(num_rows=5000)
    print("Import completed.")
