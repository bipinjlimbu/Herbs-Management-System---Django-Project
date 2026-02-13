from django.shortcuts import render, redirect
from ..models import HerbBatch, Transaction, RetailerInventory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout

def home_view(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.role == "COLLECTOR":
            context['batch_count'] = HerbBatch.objects.filter(collector=request.user).count()
            context['pending_requests'] = Transaction.objects.filter(
                collector=request.user, status='PENDING'
            ).order_by('-timestamp')

        elif request.user.role == "RETAILER":
            context['inventory_count'] = RetailerInventory.objects.filter(
                retailer=request.user
            ).values('herb_name').distinct().count()
            
            # Add this line to get the Retailer's sent requests
            context['my_pending_requests'] = Transaction.objects.filter(
                retailer=request.user, status='PENDING'
            ).order_by('-timestamp')
            
    return render(request, 'main/home_page.html', context)

@login_required
def profile_view(request, user_id):
    # Security: Only allow users to view their own profile for now
    if request.user.id != user_id:
        return redirect(f'/profile/{request.user.id}/')
        
    return render(request, 'main/profile_page.html')

@login_required
def delete_profile(request):
    if request.method == "POST":
        user = request.user
        logout(request) # Log them out first
        user.delete()   # Delete the user from DB
        messages.success(request, "Your account has been permanently deleted.")
        return redirect('/')
    return redirect('profile_view', user_id=request.user.id)