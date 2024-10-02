from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Category, Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'core/index.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)  
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:3]

    return render(request, 'item/details.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def sell(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user  # Set the user as the seller
            item.save()
            return redirect('item:items')  # Redirect to the main page after submission
    else:
        form = ItemForm()

    return render(request, 'item/sell.html', {'form': form})