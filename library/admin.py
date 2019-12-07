from django.contrib import admin

from library.models import Book, Reader

admin.site.register([Book, Reader])
