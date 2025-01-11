from django.contrib import admin
from .models import Person, Diary

# Register your models here.
admin.site.register(Person)
admin.site.register(Diary)