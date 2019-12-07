import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Reader
from users.models import CustomUser
from api.serializers.serializers import ReaderSerializer


class CreateReaderTests(APITestCase):

    def setUp(self):
        self.superuser = CustomUser.objects.create_superuser('knut', 'donaldknut@gmail.com', 'ervinpassword')
        self.client.login(username='knut', password='ervinpassword')

    def test_create_reader(self):
        url = reverse('reader-list')
        data = {'name':'Adrian', 'surname':'Holovaty'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reader.objects.count(), 1)

    def test_create_invalid_reader(self):
        url = reverse('reader-list')
        data = {'name': '', 'surname': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetReaderTests(APITestCase):

    def setUp(self):
        self.superuser = CustomUser.objects.create_superuser('knut', 'donaldknut@gmail.com', 'ervinpassword')
        self.client.login(username='knut', password='ervinpassword')
        self.reader = Reader.objects.create(name='Adrian', surname='Holovaty')

    def test_reader_list(self):
        url = reverse('reader-list')
        response = self.client.get(url, format='json')
        readers = Reader.objects.all()
        serializer = ReaderSerializer(readers, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_reader_detail(self):
        url = reverse('reader-detail', kwargs={'pk': self.reader.id})
        response = self.client.get(url, format='json')
        reader = Reader.objects.get(id=self.reader.id)
        serializer = ReaderSerializer(reader)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class UpdateReaderTests(APITestCase):

    def setUp(self):
        self.superuser = CustomUser.objects.create_superuser('knut', 'donaldknut@gmail.com', 'ervinpassword')
        self.client.login(username='knut', password='ervinpassword')
        self.reader = Reader.objects.create(name='Adrian', surname='Holovaty')

    def test_update_reader(self):
        url = reverse('reader-detail', kwargs={'pk': self.reader.id})
        response = self.client.patch(
            url, kwargs={'pk': self.reader.id},
            data=json.dumps({'name': 'Simon', 'surname': 'Willison'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Simon')
        self.assertEqual(response.data['surname'], 'Willison')


class DeleteReaderTests(APITestCase):

    def setUp(self):
        self.superuser = CustomUser.objects.create_superuser('knut', 'donaldknut@gmail.com', 'ervinpassword')
        self.client.login(username='knut', password='ervinpassword')
        self.reader = Reader.objects.create(name='Adrian', surname='Holovaty')

    def test_delete_valid_reader(self):
        url = reverse('reader-detail', kwargs={'pk': self.reader.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_reader(self):
        url = reverse('reader-detail', kwargs={'pk': self.reader.id + 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
