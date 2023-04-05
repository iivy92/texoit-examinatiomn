from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from movies.models import Studio


class StudioAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('studio-list')
        self.valid_payload = {'name': 'Studio Test'}
        self.invalid_payload = {'name': ''}

    def test_create_valid_studio(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Studio.objects.count(), 1)
        self.assertEqual(Studio.objects.get().name, 'Studio Test')

    def test_create_invalid_studio(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Studio.objects.count(), 0)

    def test_get_studio_list(self):
        Studio.objects.create(name='Studio 1')
        Studio.objects.create(name='Studio 2')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_studio_detail(self):
        studio = Studio.objects.create(name='Studio Test')
        detail_url = reverse('studio-detail', kwargs={'pk': studio.pk})
        response = self.client.get(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Studio Test')

    def test_update_studio(self):
        studio = Studio.objects.create(name='Studio Test')
        detail_url = reverse('studio-detail', kwargs={'pk': studio.pk})
        updated_payload = {'name': 'Updated Studio'}
        response = self.client.put(detail_url, updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Studio.objects.get(pk=studio.pk).name, 'Updated Studio')

    def test_delete_studio(self):
        studio = Studio.objects.create(name='Studio Test')
        detail_url = reverse('studio-detail', kwargs={'pk': studio.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Studio.objects.count(), 0)
