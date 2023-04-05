from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from movies.models import Movie, Studio, Producer
import sys

class MovieAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.studio_1 = Studio.objects.create(name='Studio 1')
        self.studio_2 = Studio.objects.create(name='Studio 2')
        self.producer_1 = Producer.objects.create(name='Producer 1')
        self.producer_2 = Producer.objects.create(name='Producer 2')

        self.movie_1 = Movie.objects.create(title='Movie 1', year=2000, winner=True)
        self.movie_1.studios.set([self.studio_1, self.studio_2])
        self.movie_1.producers.set([self.producer_1, self.producer_2])

        self.movie_2 = Movie.objects.create(title='Movie 2', year=2001, winner=False)
        self.movie_2.studios.set([self.studio_1])
        self.movie_2.producers.set([self.producer_1])
    
    
    def test_get_movie_list(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_movie_detail(self):
        url = reverse('movie-detail', kwargs={'pk': self.movie_1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Movie 1')
        self.assertEqual(response.data['year'], 2000)
    
    def test_create_movie(self):
        url = reverse('movie-list')
        data = {
            'title': 'Movie 3',
            'year': 2002,
            'studios': [{"name": "Studio Test 1"}],
            'producers': [{"name": "Producer Test 1"}],
            'winner': True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.count(), 3)
        movie = Movie.objects.get(title='Movie 3')
        self.assertEqual(movie.year, 2002)
        self.assertEqual(movie.studios.count(), 1)
        self.assertEqual(movie.studios.first().name, 'Studio Test 1')
        self.assertEqual(movie.producers.count(), 1)
        self.assertEqual(movie.producers.first().name, 'Producer Test 1')

    def test_create_movie_invalid_data(self):
        url = reverse('movie-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_movie(self):
        url = reverse('movie-detail', args=[self.movie_1.pk])
        data = {
            'title': 'Movie 1 Updated',
            'year': 2003,
            'studios': [{'name': 'Studio Update 1'}],
            'producers': [{'name': 'Producer Update 1'}],
            'winner': False,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.count(), 2)
        movie = Movie.objects.get(pk=self.movie_1.pk)
        self.assertEqual(movie.title, 'Movie 1 Updated')
        self.assertEqual(movie.year, 2003)
        self.assertEqual(movie.studios.count(), 1)
        self.assertEqual(movie.studios.first().name, 'Studio Update 1')
        self.assertEqual(movie.producers.count(), 1)
        self.assertEqual(movie.producers.first().name, 'Producer Update 1')

    def test_update_movie_invalid_data(self):
        url = reverse('movie-detail', args=[self.movie_1.pk])
        data = {
            'year': 'Invalid Year'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
