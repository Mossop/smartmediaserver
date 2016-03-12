from django.contrib import admin

from .models import *

admin.site.register(PhysicalFolder)
admin.site.register(VirtualFolder)
admin.site.register(Photo)
