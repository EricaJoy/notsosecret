from django.contrib import admin
from secretkeeper.models import Secret

# Register your models here.
# class SecretAdmin(admin.ModelAdmin):
#     fields = ['secret_text']
#     readonly_fields = ('timestamp',)

admin.site.register(Secret)