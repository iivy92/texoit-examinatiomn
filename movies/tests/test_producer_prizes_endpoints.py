from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse

from movies.models import Producer, Movie
from movies.views import ProducerPrizesView


class ProducerPrizesViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Criando produtores e filmes para os testes
        cls.producer1 = Producer.objects.create(name='Producer 1')
        cls.producer2 = Producer.objects.create(name='Producer 2')
        cls.producer3 = Producer.objects.create(name='Producer 3')

        cls.movie1 = Movie.objects.create(
            title='Movie 1',
            year=2021,
            winner=True
        )
        cls.movie1.producers.add(cls.producer1)
        cls.movie1.producers.add(cls.producer2)

        cls.movie2 = Movie.objects.create(
            title='Movie 2',
            year=2020,
            winner=True
        )
        cls.movie2.producers.add(cls.producer1)
        cls.movie2.producers.add(cls.producer3)

        cls.movie3 = Movie.objects.create(
            title='Movie 3',
            year=2019,
            winner=True
        )
        cls.movie3.producers.add(cls.producer2)

        cls.movie4 = Movie.objects.create(
            title='Movie 4',
            year=2018,
            winner=True
        )
        cls.movie4.producers.add(cls.producer3)

        cls.movie5 = Movie.objects.create(
            title='Movie 5',
            year=2017,
            winner=False
        )
        cls.movie5.producers.add(cls.producer1)

        cls.url = reverse('producer-prizes')

    def test_producer_prizes_view_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

        data = response.json()

        # Verificando se a resposta contém as chaves 'min' e 'max'
        self.assertIn('min', data)
        self.assertIn('max', data)

        # Verificando o resultado para o menor intervalo entre vitórias
        min_data = data['min']
        self.assertEqual(len(min_data), 1)

        expected_min_data = [
            {
                'producer': self.producer1.name,
                'interval': 1,
                'previousWin': self.movie2.year,
                'followingWin': self.movie1.year,
            }
        ]

        self.assertCountEqual(min_data, expected_min_data)

        # Verificando o resultado para o maior intervalo entre vitórias
        max_data = data['max']
        self.assertEqual(len(max_data), 2)

        expected_max_data = [
            {
                'producer': self.producer3.name,
                'interval': 2,
                'previousWin': self.movie4.year,
                'followingWin': self.movie2.year,
            },
            {
                'producer': self.producer2.name,
                'interval': 2,
                'previousWin': self.movie3.year,
                'followingWin': self.movie1.year,
            },
        ]

        self.assertCountEqual(max_data, expected_max_data)
