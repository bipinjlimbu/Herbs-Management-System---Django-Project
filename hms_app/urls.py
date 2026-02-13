from django.urls import path
from .views.main import home_view
from .views.auth import register_view, login_view, logout_view
from .views.herb import add_herb_view, my_collections_view, marketplace_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-batch/', add_herb_view, name='add_batch'),
    path('my-batches/', my_collections_view, name='my_batches'),
    path('marketplace/', marketplace_view, name='marketplace'),
]
