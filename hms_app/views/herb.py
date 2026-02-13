from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from ..models import HerbBatch, RetailerInventory

@login_required
def add_herb_view(request):
    if request.user.role != 'COLLECTOR':
        messages.error(request, "Access denied. Only collectors can list herbs.")
        return redirect('/')

    if request.method == 'POST':
        name = request.POST.get('name')
        total_quantity = request.POST.get('total_quantity')
        harvest_date = request.POST.get('harvest_date')

        HerbBatch.objects.create(
            name=name,
            collector=request.user,
            total_quantity=total_quantity,
            remaining_quantity=total_quantity, 
            harvest_date=harvest_date,
            is_available=True
        )

        messages.success(request, f"Batch for {name} added successfully!")
        return redirect('/') 
    
    return render(request, 'pages/add_herb.html')

@login_required
def my_collections_view(request):
    # Fetch batches where the collector is the logged-in user
    batches = HerbBatch.objects.filter(collector=request.user).order_by('-harvest_date')
    
    return render(request, 'pages/my_collections.html', {'batches': batches}) 

def marketplace_view(request):
    # Filter for available batches with remaining stock > 0
    available_batches = HerbBatch.objects.filter(
        is_available=True, 
        remaining_quantity__gt=0
    ).order_by('-harvest_date')
    
    return render(request, 'pages/marketplace.html', {
        'available_batches': available_batches
    })
    
@login_required
def my_stock_view(request):
    context = {}
    if request.user.role == "COLLECTOR":
        # Collectors usually track specific batches for harvest dates
        context['collector_stock'] = HerbBatch.objects.filter(collector=request.user)
    else:
        # RETAILER: Group by herb_name and sum the current_stock
        context['retailer_stock'] = RetailerInventory.objects.filter(
            retailer=request.user
        ).values('herb_name').annotate(
            total_quantity=Sum('current_stock')
        ).order_by('herb_name')
        
    return render(request, 'pages/my_stock.html', context)