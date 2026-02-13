from django.shortcuts import render
from ..models import HerbBatch, Transaction, RetailerInventory

def home_view(request):
    context = {}
    
    if request.user.is_authenticated:
        if request.user.role == "COLLECTOR":
            # 1. Total count of batches listed by this collector
            context['batch_count'] = HerbBatch.objects.filter(collector=request.user).count()
            
            # 2. Fetch only PENDING requests sent to this collector
            context['pending_requests'] = Transaction.objects.filter(
                collector=request.user, 
                status='PENDING'
            ).order_by('-timestamp')

        elif request.user.role == "RETAILER":
            # 1. Total items in their own inventory
            context['inventory_count'] = RetailerInventory.objects.filter(retailer=request.user).count()
            
            # 2. Optional: Show their own pending requests sent to collectors
            context['my_requests'] = Transaction.objects.filter(
                retailer=request.user, 
                status='PENDING'
            ).order_by('-timestamp')
            
    return render(request, 'main/home_page.html', context)