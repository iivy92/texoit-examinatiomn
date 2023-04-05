from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from movies.models import Producer

class ProducerAPITest(APITestCase):
    def setUp(self):
        self.producer = Producer.objects.create(
            name='Steven Spielberg'
        )

    def test_list_producers(self):
        url = reverse('producer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.producer.name)

    def test_create_producer(self):
        url = reverse('producer-list')
        data = {
            'name': 'Quentin Tarantino'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producer.objects.count(), 2)
        producer = Producer.objects.last()
        self.assertEqual(producer.name, data['name'])

    def test_retrieve_producer(self):
        url = reverse('producer-detail', args=[self.producer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.producer.name)

    def test_update_producer(self):
        url = reverse('producer-detail', args=[self.producer.id])
        data = {
            'name': 'Steven Spielberg II'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.producer.refresh_from_db()
        self.assertEqual(self.producer.name, data['name'])

    def test_delete_producer(self):
        url = reverse('producer-detail', args=[self.producer.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Producer.objects.count(), 0)

    def test_create_producer_invalid_data(self):
        url = reverse('producer-list')
        data = {
            'name': '',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Producer.objects.count(), 1)

    def test_update_producer_invalid_data(self):
        url = reverse('producer-detail', args=[self.producer.id])
        data = {
            'name': '',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.producer.refresh_from_db()
        self.assertNotEqual(self.producer.name, data['name'])
