from django.contrib import admin

from .models import Book, History

# Register your models here.
admin.site.register(Book)
admin.site.register(History)
