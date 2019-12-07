from rest_framework.routers import SimpleRouter
from django.urls import path

from api.views import BookViewSet, ReaderViewSet, book_csv_report


router = SimpleRouter()
router.register('book', BookViewSet, base_name='book')
router.register('reader', ReaderViewSet, base_name='reader')

urlpatterns = [*router.urls, path('book_csv_report', book_csv_report, name='book-csv-report')]
