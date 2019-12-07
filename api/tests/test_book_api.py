import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Book, Reader
from users.models import CustomUser
from api.serializers.serializers import BookNestedSerializer


class CreateBookTests(APITestCase):

    def setUp(self):
        self.superuser = CustomUser.objects.create_superuser('knut', 'donaldknut@gmail.com', 'ervinpassword')
        self.client.login(username='knut', password='ervinpassword')

    def test_create_book(self):
        url = reverse('book-list')
        data = {'title': 'Two Scoops of Django', 'author': 'Audrey Greenfeld'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)

    def test_create_invalid_book(self):
        url = reverse('book-list')
        data = {'title': '', 'author': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_existing_book(self):
        django_book = Book.objects.create(title='Django for beginners', author='William Wincent')
        django_book.save()
        url = reverse('book-list')
        data = {'title': 'Django for beginners', 'author': 'William Wincent'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetBookTests(APITestCase):

    def setUp(self):
        self.superuser = CustomUser.objects.create_superuser('knut', 'donaldknut@gmail.com', 'ervinpassword')
        self.client.login(username='knut', password='ervinpassword')
        self.django_book = Book.objects.create(title='Django for beginners', author='William Wincent')

    def test_book_list(self):
        url = reverse('book-list')
        response = self.client.get(url, format='json')
        books = Book.objects.all()
        serializer = BookNestedSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_book_detail(self):
        url = reverse('book-detail', kwargs={'pk': self.django_book.id})
        response = self.client.get(url, format='json')
        django_book = Book.objects.get(id=self.django_book.id)
        serializer = BookNestedSerializer(django_book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class UpdateBookTests(APITestCase):

    def setUp(self):
        self.superuser = CustomUser.objects.create_superuser('knut', 'donaldknut@gmail.com', 'ervinpassword')
        self.client.login(username='knut', password='ervinpassword')
        self.reader = Reader.objects.create(name='Adrian', surname='Holovaty')
        self.django_book = Book.objects.create(title='Django for beginners', author='William Wincent')
        self.flask_book = Book.objects.create(title='Flask Mega-Tutorial', author='Miguel Grinberg', reader=self.reader)

    def test_update_book(self):
        url = reverse('book-detail', kwargs={'pk': self.django_book.id})
        response = self.client.patch(
            url, kwargs={'pk': self.django_book.id},
            data=json.dumps({'title': 'Django for professionals', 'author': 'William S. Wincent'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django for professionals')
        self.assertEqual(response.data['author'], 'William S. Wincent')

    def test_assign_reader(self):
        url = reverse('book-detail', kwargs={'pk': self.django_book.id})
        response = self.client.patch(
            url, kwargs={'pk': self.django_book.id},
            data=json.dumps({'reader': self.reader.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reader'], self.reader.id)
        self.assertIsNotNone(response.data['issued_at'])

    def test_deassign_reader(self):
        url = reverse('book-detail', kwargs={'pk': self.flask_book.id})
        response = self.client.patch(
            url, kwargs={'pk': self.flask_book.id},
            data=json.dumps({'reader': None}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['reader'], self.reader.id)
        self.assertIsNone(response.data['issued_at'])


class DeleteBookTests(APITestCase):

    def setUp(self):
        self.superuser = CustomUser.objects.create_superuser('knut', 'donaldknut@gmail.com', 'ervinpassword')
        self.client.login(username='knut', password='ervinpassword')
        self.django_book = Book.objects.create(title='Django for beginners', author='William Wincent')

    def test_delete_valid_book(self):
        url = reverse('book-detail', kwargs={'pk': self.django_book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_book(self):
        url = reverse('book-detail', kwargs={'pk': self.django_book.id+1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

