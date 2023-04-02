from rest_framework.test import APITestCase
from rest_framework import status
from movies.models import Movie, Studio, Producer

class MovieAPITests(APITestCase):
    
    def setUp(self):
        self.studio1 = Studio.objects.create(name='Studio 1')
        self.studio2 = Studio.objects.create(name='Studio 2')
        self.producer1 = Producer.objects.create(name='Producer 1')
        self.producer2 = Producer.objects.create(name='Producer 2')
        self.movie1 = Movie.objects.create(title='Movie 1', year=2022, winner=True)
        self.movie1.studios.set([self.studio1, self.studio2])
        self.movie1.producers.set([self.producer1, self.producer2])
        self.movie2 = Movie.objects.create(title='Movie 2', year=2023, winner=False)
        self.movie2.studios.set([self.studio1])
        self.movie2.producers.set([self.producer2])

    def test_list_movies(self):
        url = '/movies/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_movie(self):
        url = '/movies/'
        data = {'title': 'New Movie', 'year': 2024, 'winner': True,
                'studios': [self.studio1.id], 'producers': [self.producer1.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 3)
        self.assertEqual(Movie.objects.last().title, 'New Movie')

    def test_retrieve_movie(self):
        url = '/movies/{}/'.format(self.movie1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Movie 1')

    def test_update_movie(self):
        url = '/movies/{}/'.format(self.movie1.id)
        data = {'title': 'Updated Movie'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.get(id=self.movie1.id).title, 'Updated Movie')

    def test_partial_update_movie(self):
        url = '/movies/{}/'.format(self.movie1.id)
        data = {'winner': False}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Movie.objects.get(id=self.movie1.id).winner)

    def test_delete_movie(self):
        url = '/movies/{}/'.format(self.movie1.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 1)
