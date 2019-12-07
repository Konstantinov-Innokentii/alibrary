from rest_framework.routers import SimpleRouter

from api.views import BookViewSet, ReaderViewSet


router = SimpleRouter()
router.register('book', BookViewSet, base_name='book')
router.register('reader', ReaderViewSet, base_name='reader')

urlpatterns = router.urls
