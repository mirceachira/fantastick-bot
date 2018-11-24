from django.urls import include, path
from messenger_bot import views


urlpatterns = [
    path('', views.index, name='index'),
]
