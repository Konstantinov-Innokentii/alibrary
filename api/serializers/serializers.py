from rest_framework import serializers
from library.models import Book, Reader

from api.serializers.custom_serializers import DynamicFieldsModelSerializer


class BookSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'reader', 'issued_at']
        read_only_fields = ('issued_at',)


class BookNestedSerializer(BookSerializer):
    class Meta(BookSerializer.Meta):
        depth = 1


class ReaderSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True, fields=['id', 'title', 'author', 'issued_at'])

    class Meta:
        model = Reader
        fields = ['id', 'name', 'surname', 'books']
