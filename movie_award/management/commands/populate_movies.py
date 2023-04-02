from django.core.management.base import BaseCommand
import tablib
from movie_award.models import Movie, Studio, Producer
import csv

class Command(BaseCommand):
    help = 'Import movies from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The CSV file to import from')

    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename, 'r') as csvfile:
            data = csv.reader(csvfile, delimiter=';')
            data.__next__()
            for row in data:
                movies = dict(
                    year=row[0],
                    title=row[1],
                    winner=True if row[4].lower() == 'yes' else False
                )
                studios = []
                for studio_name in row[2].split(','):
                    studio, _ = Studio.objects.get_or_create(name=studio_name.strip())
                    studios.append(studio)
                
                producers = []
                for producer_name in row[3].replace("and", ",").split(','):
                    producer, _ = Producer.objects.get_or_create(name=producer_name.strip())
                    producers.append(producer)


                movie, _ = Movie.objects.get_or_create(**movies)
                movie.studios.set(studios)
                movie.producers.set(producers)
            
            self.stdout.write(self.style.SUCCESS('Movies imported successfully.'))
