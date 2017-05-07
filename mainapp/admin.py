from django.contrib import admin

from mainapp.models import User, Document, Error
# Register your models here.
admin.site.register(User)
admin.site.register(Document)
admin.site.register(Error)