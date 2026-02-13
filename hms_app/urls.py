from django.urls import path
from .views.main import delete_profile, home_view, profile_view
from .views.auth import register_view, login_view, logout_view
from .views.herb import add_herb_view, my_collections_view, marketplace_view, my_stock_view
from .views.transactions import purchase_request_view, approve_transaction, reject_transaction, transaction_history_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-batch/', add_herb_view, name='add_batch'),
    path('my-batches/', my_collections_view, name='my_batches'),
    path('marketplace/', marketplace_view, name='marketplace'),
    path('purchase/<int:batch_id>/', purchase_request_view, name='purchase_request'),
    path('approve/<int:transaction_id>/', approve_transaction, name='approve_transaction'),
    path('reject/<int:transaction_id>/', reject_transaction, name='reject_transaction'),
    path('my-stock/', my_stock_view, name='my_stock'),
    path('transactions/', transaction_history_view, name='transaction_history'),
    path('profile/<int:user_id>/', profile_view, name='profile_view'),
    path('profile/delete/', delete_profile, name='delete_profile'),
]
