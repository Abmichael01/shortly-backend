from django.contrib import admin
from .models import Url, Click



admin.site.register([Url, Click])
