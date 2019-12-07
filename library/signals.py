from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from library.models import Book


@receiver(pre_save, sender=Book)
def set_book_issued(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.id)
    except sender.DoesNotExist:
        if instance.reader is not None:
            instance.issued_at = timezone.now()
    else:
        if instance.reader is None:
            instance.issued_at = None
        elif obj.reader != instance.reader:
            instance.issued_at = timezone.now()
