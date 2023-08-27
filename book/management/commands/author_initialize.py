from book.models import Author

from django.utils.text import slugify
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Initialize some author at database"

    def handle(self, *args, **options):
        authors = ["george orwell", "J.R.R. Tolkien", "J.K. Rowling", "fyodor dostoevsky", "leo tolstoy",
                   "ahmad shamlou", "Jalal Al-e-Ahmad"]
        for author in authors:
            Author.objects.create(name=author, slug=slugify(author), city_id=1)
        self.stdout.write('Author Objects are created')
