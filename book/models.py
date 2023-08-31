from user.models import User

from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


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
    availability = models.IntegerField()
    in_reserve = models.PositiveIntegerField()
    version = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.price < 0:
            raise ValidationError('price cannot be negative')
        super(Book, self).save(*args, **kwargs)


class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='books_reserved')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reserved')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    cost = models.PositiveBigIntegerField()

    def save(self, *args, **kwargs):
        if self.cost < 0:
            raise ValidationError('cost cannot be negative')
        if (self.end_date - self.start_date).days > 14:
            raise ValidationError('reserve days cannot more than 14 days')


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
