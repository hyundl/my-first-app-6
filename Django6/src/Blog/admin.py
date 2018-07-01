from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(PostType)
admin.site.register(Image)
admin.site.register(File)

