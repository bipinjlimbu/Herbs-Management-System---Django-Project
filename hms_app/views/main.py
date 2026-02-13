from django.shortcuts import render
from ..models import HerbBatch

def home_view(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.role == "COLLECTOR":
            context['batch_count'] = HerbBatch.objects.filter(collector=request.user).count()
        elif request.user.role == "RETAILER":
            # Assuming you have RetailerInventory model imported
            from ..models import RetailerInventory
            context['inventory_count'] = RetailerInventory.objects.filter(retailer=request.user).count()
        
    return render(request, 'main/home_page.html', context)
