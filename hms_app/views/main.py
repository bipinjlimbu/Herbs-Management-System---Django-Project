from django.shortcuts import render
from ..models import HerbBatch, Transaction, RetailerInventory

def home_view(request):
    context = {}
    
    if request.user.is_authenticated:
        if request.user.role == "COLLECTOR":
            context['batch_count'] = HerbBatch.objects.filter(collector=request.user).count()
            context['pending_requests'] = Transaction.objects.filter(
                collector=request.user, 
                status='PENDING'
            ).order_by('-timestamp')

        elif request.user.role == "RETAILER":
            # Count unique herb names instead of total rows
            unique_items_count = RetailerInventory.objects.filter(
                retailer=request.user
            ).values('herb_name').distinct().count()
            
            context['inventory_count'] = unique_items_count
            
    return render(request, 'main/home_page.html', context)