

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=200)),
                ("gender", models.CharField(blank=True, max_length=10)),
                ("image_url", models.URLField(blank=True)),
                ("about", models.TextField(blank=True)),
                ("fans_count", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(db_index=True, max_length=200)),
                ("isbn", models.CharField(max_length=13, unique=True)),
                ("isbn13", models.CharField(blank=True, max_length=13)),
                ("asin", models.CharField(blank=True, max_length=10)),
                ("language", models.CharField(max_length=3)),
                ("average_rating", models.FloatField(default=0)),
                ("ratings_count", models.IntegerField(default=0)),
                ("text_reviews_count", models.IntegerField(default=0)),
                ("publisher", models.CharField(max_length=200)),
                ("num_pages", models.IntegerField()),
                ("description", models.TextField(blank=True)),
                ("genre", models.CharField(db_index=True, max_length=100)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="books",
                        to="api.author",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.book"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorites",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "book")},
            },
        ),
    ]
