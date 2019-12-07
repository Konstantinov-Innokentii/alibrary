from django.test import TestCase

from library.models import Book, Reader


class ReaderTests(TestCase):
    def setUp(self):
        self.reader = Reader.objects.create(name='Simon', surname='Willison')

    def test_new_reader(self):
        reader = Reader.objects.get(id=self.reader.id)
        self.assertEqual(f'{reader.name}', 'Simon')
        self.assertEqual(f'{reader.surname}', 'Willison')
        self.assertFalse(reader.books.exists())

    def test_reader_str(self):
        reader = Reader.objects.get(id=self.reader.id)
        self.assertEqual(str(reader), 'Simon Willison')


class BookTests(TestCase):
    def setUp(self):
        self.django_book = Book.objects.create(title='Django for beginners', author='William Wincent')

    def test_new_book(self):
        django_book = Book.objects.get(id=self.django_book.id)
        self.assertEqual(f'{django_book.title}', 'Django for beginners')
        self.assertEqual(f'{django_book.author}', 'William Wincent')
        self.assertIsNone(django_book.issued_at)
        self.assertIsNone(django_book.reader)

    def test_book_str(self):
        django_book = Book.objects.get(id=self.django_book.id)
        self.assertEqual(str(django_book), 'Django for beginners')


class LibraryTests(TestCase):

    def setUp(self):
        self.reader_with_book = Reader.objects.create(name='Adrian', surname='Holovaty')
        self.flask_book = Book.objects.create(title='Flask Mega-Tutorial', author='Miguel Grinberg',
                                              reader=self.reader_with_book)

    def test_book_issued(self):
        reader_with_book = Reader.objects.get(id=self.reader_with_book.id)
        flask_book = Book.objects.get(id=self.flask_book.id)
        self.assertIsNotNone(flask_book.issued_at)
        self.assertEqual(flask_book.reader, reader_with_book)

    def test_reader_has_book(self):
        reader_with_book = Reader.objects.get(id=self.reader_with_book.id)
        self.assertTrue(reader_with_book.books.exists())
