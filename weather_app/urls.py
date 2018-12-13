from django.urls import path
from django.conf.urls import url
from . import views

app_name="weather_app"

urlpatterns = [
    path('',views.index,name='index'),
    path('delete/<id>', views.delete, name='delete'),
]
