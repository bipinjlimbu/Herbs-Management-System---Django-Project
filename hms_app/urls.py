from django.urls import path
from .views.main import home_view

urlpatterns = [
    path('', home_view, name='home'),
]
