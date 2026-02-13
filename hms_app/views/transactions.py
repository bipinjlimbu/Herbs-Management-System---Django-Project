from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import HerbBatch, RetailerInventory, Transaction

@login_required
def purchase_request_view(request, batch_id):
    batch = get_object_or_404(HerbBatch, id=batch_id)
    
    if request.method == 'POST':
        qty = float(request.POST.get('quantity'))
        price = request.POST.get('total_price')

        # Just create the request, do NOT subtract stock yet
        Transaction.objects.create(
            collector=batch.collector,
            retailer=request.user,
            batch=batch,
            quantity_bought=qty,
            total_price=price,
            status='PENDING'
        )
        messages.success(request, "Purchase request sent! Waiting for collector approval.")
        return redirect('/')
    
    return render(request, 'pages/purchase_page.html', {'batch': batch})

@login_required
def approve_transaction(request, transaction_id):
    tx = get_object_or_404(Transaction, id=transaction_id, collector=request.user)
    
    if tx.status != 'PENDING':
        messages.error(request, "This transaction has already been processed.")
        return redirect('/')

    # 1. Deduct stock from the actual Batch
    batch = tx.batch
    if batch.remaining_quantity >= tx.quantity_bought:
        batch.remaining_quantity -= tx.quantity_bought
        if batch.remaining_quantity == 0:
            batch.is_available = False
        batch.save()

        # 2. Update Transaction Status
        tx.status = 'APPROVED'
        tx.save()

        # 3. Add to Retailer's Inventory
        RetailerInventory.objects.create(
            retailer=tx.retailer,
            herb_name=batch.name,
            current_stock=tx.quantity_bought,
            original_batch=batch
        )
        messages.success(request, "Transaction approved and stock transferred.")
    else:
        messages.error(request, "Not enough stock to fulfill this request.")
    
    return redirect('/')

@login_required
def reject_transaction(request, transaction_id):
    # Ensure only the collector assigned to this transaction can reject it
    tx = get_object_or_404(Transaction, id=transaction_id, collector=request.user)
    
    if request.method == 'POST':
        if tx.status == 'PENDING':
            tx.status = 'REJECTED'
            tx.save()
            messages.info(request, f"Purchase request for {tx.batch.name} has been rejected.")
        else:
            messages.error(request, "This transaction has already been processed.")
            
    return redirect('/')

@login_required
def transaction_history_view(request):
    status_filter = request.GET.get('status')
    
    # 1. Start with the role-based filter
    if request.user.role == "COLLECTOR":
        transactions = Transaction.objects.filter(collector=request.user)
    else:
        transactions = Transaction.objects.filter(retailer=request.user)
    
    # 2. STRICKLY EXCLUDE PENDING: This hides pending from the "All" view too
    transactions = transactions.exclude(status='PENDING')
    
    # 3. Apply status filter for Approved/Rejected if clicked
    if status_filter and status_filter != 'ALL':
        transactions = transactions.filter(status=status_filter)
        
    transactions = transactions.order_by('-timestamp')
    
    return render(request, 'pages/transactions.html', {
        'transactions': transactions,
        'current_filter': status_filter or 'ALL'
    })