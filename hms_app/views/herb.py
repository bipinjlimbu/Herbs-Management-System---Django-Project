from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import HerbBatch

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