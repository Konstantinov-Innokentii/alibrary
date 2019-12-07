from rest_framework import viewsets
from django.db import IntegrityError
from rest_framework.exceptions import APIException

from library.models import Book, Reader
from api.serializers.serializers import BookSerializer, ReaderSerializer, BookNestedSerializer
from api.serializers.mixins import ReadWriteSerializerMixin


class BookViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()
    read_serializer_class = BookNestedSerializer
    write_serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as exc:
            raise APIException(detail=exc)


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
