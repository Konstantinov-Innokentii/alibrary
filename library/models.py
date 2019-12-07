from django.db import models


class Reader(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    issued_at = models.DateTimeField(null=True, blank=True)

    reader = models.ForeignKey(Reader, on_delete=models.SET_NULL, related_name='books', null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'], name='unique_title_author')
        ]

    def __str__(self):
        return self.title
