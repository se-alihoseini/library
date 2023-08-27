from django.db import models
from django.utils.text import slugify


class Book(models.Model):
    title = models.CharField(max_length=30)
    slug = models.CharField(unique=True, blank=True, null=True)
    description = models.TextField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='author_book')
    genre = models.ManyToManyField('Genre', related_name='genre_books')
    publication_date = models.DateField()
    isbn = models.CharField(max_length=30)
    price = models.PositiveBigIntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(unique=True, null=True, blank=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='city_authors')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)


class City(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)
