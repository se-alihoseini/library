from book.models import City

from django.utils.text import slugify
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Initialize some city at database"

    def handle(self, *args, **options):
        cities = ["Tehran", "Isfahan", "Shiraz", "Mashhad", "Tabriz", "Yazd", "Kerman", "Ahvaz", "Qom", "Rasht",
                  "Kermanshah", "Bandar Abbas", "Hamadan", "Kish Island", "Ardabil"]
        for city in cities:
            City.objects.create(name=city, slug=slugify(city))
        self.stdout.write('City Objects are created')
