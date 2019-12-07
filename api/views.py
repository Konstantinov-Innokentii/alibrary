import csv
from rest_framework import viewsets
from django.http import HttpResponse
from django.db import IntegrityError
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view

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


@api_view()
def book_csv_report(request):
    header = ['Title', 'Reader', 'Issued At']

    local_today = timezone.localtime(timezone.now()).date()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="library_report_{local_today}.csv"'

    writer = csv.writer(response)
    writer.writerow(header)
    for book in Book.objects.all():
        row = [book.title, book.reader, book.issued_at.strftime('%Y-%m-%d %H:%M') if book.issued_at is not None else '']
        writer.writerow(row)

    return response
