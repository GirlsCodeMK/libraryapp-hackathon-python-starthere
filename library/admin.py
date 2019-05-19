from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.

from library.models import Book, Copy, Loan, Configuration, UserMicrobit, Category

admin.site.register(Book)
admin.site.register(Copy)
admin.site.register(Loan)
admin.site.register(UserMicrobit)
admin.site.register(Configuration)
admin.site.register(Category)

TokenAdmin.raw_id_fields = ('user',)
