from book.models import Genre

from django.utils.text import slugify
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Initialize some genre at database"

    def handle(self, *args, **options):
        genres = ["mystery", "fantasy", "horror", "romance", "biography", "science fiction"]
        for genre in genres:
            Genre.objects.create(name=genre, slug=slugify(genre))
        self.stdout.write('Genre Objects are created')
