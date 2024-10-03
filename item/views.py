from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Category, Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

CART = []

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    cart_count = sum(item['quantity'] for item in CART)

    return render(request, 'core/index.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'cart_count': cart_count
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)  
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:3]
    
    cart_count = sum(item['quantity'] for item in CART)

    return render(request, 'item/details.html', {
        'item': item,
        'related_items': related_items,
        'cart_count': cart_count
    })

@login_required
def sell(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:items')
    else:
        form = ItemForm()

    cart_count = sum(item['quantity'] for item in CART)

    return render(request, 'item/sell.html', {'form': form, 'cart_count': cart_count})

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    for cart_item in CART:
        if cart_item['item'].id == item_id:
            cart_item['quantity'] += 1
            cart_count = sum(item['quantity'] for item in CART)
            if request.is_ajax():
                return JsonResponse({'success': True, 'cart_count': cart_count})
            return redirect('item:checkout')
    CART.append({'item': item, 'quantity': 1})
    cart_count = sum(item['quantity'] for item in CART)
    if request.is_ajax():
        return JsonResponse({'success': True, 'cart_count': cart_count})
    return redirect('item:checkout')

@login_required
def remove_from_cart(request, item_id):
    for cart_item in CART:
        if cart_item['item'].id == item_id:
            CART.remove(cart_item)
            break
    return redirect('item:checkout')

@login_required
def checkout(request):
    cart_items = []
    total_price = 0
    for cart_item in CART:
        item = cart_item['item']
        quantity = cart_item['quantity']
        subtotal = item.price * quantity
        total_price += subtotal
        cart_items.append({
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'quantity': quantity,
            'subtotal': subtotal
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': sum(item['quantity'] for item in CART)
    }
    return render(request, 'item/checkout.html', context)
