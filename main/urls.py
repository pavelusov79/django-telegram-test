from django.contrib.auth.views import LogoutView
from django.urls import path

from main import views


urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
