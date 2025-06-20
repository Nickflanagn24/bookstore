# Generated by Django 4.2.7 on 2025-06-17 21:32

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("biography", models.TextField(blank=True, null=True)),
                (
                    "photo",
                    models.URLField(
                        blank=True, help_text="Author photo URL", null=True
                    ),
                ),
                (
                    "google_books_id",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("is_featured", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Author",
                "verbose_name_plural": "Authors",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "google_books_id",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("isbn_10", models.CharField(blank=True, max_length=10, null=True)),
                ("isbn_13", models.CharField(blank=True, max_length=13, null=True)),
                ("title", models.CharField(max_length=300)),
                ("subtitle", models.CharField(blank=True, max_length=300, null=True)),
                ("publisher", models.CharField(blank=True, max_length=200, null=True)),
                ("published_date", models.DateField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("page_count", models.PositiveIntegerField(blank=True, null=True)),
                ("language", models.CharField(default="en", max_length=10)),
                (
                    "thumbnail",
                    models.URLField(
                        blank=True, help_text="Small book cover image URL", null=True
                    ),
                ),
                (
                    "cover_image",
                    models.URLField(
                        blank=True, help_text="Large book cover image URL", null=True
                    ),
                ),
                (
                    "main_category",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("stock_quantity", models.PositiveIntegerField(default=0)),
                ("is_available", models.BooleanField(default=True)),
                ("is_featured", models.BooleanField(default=False)),
                (
                    "average_rating",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=3,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5),
                        ],
                    ),
                ),
                ("ratings_count", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "authors",
                    models.ManyToManyField(related_name="books", to="books.author"),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True, related_name="books", to="books.category"
                    ),
                ),
            ],
            options={
                "verbose_name": "Book",
                "verbose_name_plural": "Books",
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["title"], name="books_book_title_d3218d_idx"),
                    models.Index(
                        fields=["google_books_id"], name="books_book_google__da53e2_idx"
                    ),
                    models.Index(
                        fields=["isbn_13"], name="books_book_isbn_13_a77f18_idx"
                    ),
                    models.Index(
                        fields=["is_featured"], name="books_book_is_feat_81be5a_idx"
                    ),
                    models.Index(
                        fields=["is_available"], name="books_book_is_avai_7b1023_idx"
                    ),
                ],
            },
        ),
    ]
