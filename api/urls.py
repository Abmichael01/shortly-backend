from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt 

urlpatterns = [
    path("shorten-url/", views.shorten_url, name="shorten-url"),
    path("get-urls/", views.get_urls, name="get-urls"),
    path("get-url/<str:pk>/", csrf_exempt(views.get_url), name="get-url"),
    path("delete-url/<str:pk>/", views.delete_url, name="delete-url"),
    path("get-stats/<str:pk>/", views.get_stats, name="get-stats"),
]
