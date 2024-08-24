from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_alter_book_isbn"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="author_name",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
