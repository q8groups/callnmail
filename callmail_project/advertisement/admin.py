from django.contrib import admin

from .models import Advertisement, UserProfile,Banner

admin.site.register(Advertisement)

admin.site.register(UserProfile)
admin.site.register(Banner)
