import csv
import io
from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from library.models import Book, Reader


class BookCsvReportTests(TestCase):

    def setUp(self):
        self.superuser = CustomUser.objects.create_superuser('knut', 'donaldknut@gmail.com', 'ervinpassword')
        self.client.login(username='knut', password='ervinpassword')

    def test_report_with_books(self):
        reader = Reader.objects.create(name='Adrian', surname='Holovaty')
        django_book = Book.objects.create(title='Django for beginners', author='William Wincent', reader=reader)

        reader.save()
        django_book.save()

        url = reverse('book-csv-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)
        header = body.pop(0)
        self.assertEqual(header, ['Title', 'Reader', 'Issued At'])
        content = body.pop(0)
        django_book = Book.objects.get(id=django_book.id)
        self.assertEqual(content, [django_book.title, str(django_book.reader), django_book.issued_at.strftime('%Y-%m-%d %H:%M')])

    def test_report_book_without_user(self):
        django_book = Book.objects.create(title='Django for beginners', author='William Wincent')
        django_book.save()

        url = reverse('book-csv-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)
        header = body.pop(0)
        self.assertEqual(header, ['Title', 'Reader', 'Issued At'])
        content = body.pop(0)
        django_book = Book.objects.get(id=django_book.id)
        self.assertEqual(content,
                         [django_book.title, '', ''])

    def test_report_without_books(self):
        url = reverse('book-csv-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)
        header = body.pop(0)
        self.assertEqual(header, ['Title', 'Reader', 'Issued At'])
        self.assertEqual(len(body), 0)
