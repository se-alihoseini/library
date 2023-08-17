from django.db import models
from django.utils.text import slugify


class Book(models.Model):
    title = models.CharField(max_length=30)
    slug = models.CharField(unique=True, blank=True, null=True)
    author = models.ManyToManyField('Author')
    genre = models.ForeignKey('Genre', related_name='genre_book', on_delete=models.CharField)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=30)
    price = models.BigIntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=50, unique=True)


class City(models.Model):
    name = models.CharField(max_length=30)
