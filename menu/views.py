from django.shortcuts import get_object_or_404, render

from .models import Category, MenuItem


def menu_list(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    menu_items = MenuItem.objects.select_related('category')

    active_category = None
    if category_slug:
        active_category = categories.filter(slug=category_slug).first()
        if active_category:
            menu_items = menu_items.filter(category=active_category)
        # unmatched slug falls back to "no filter" (contracts/web-routes.md)

    context = {
        'menu_items': menu_items,
        'categories': categories,
        'active_category': active_category,
    }
    return render(request, 'menu/menu_list.html', context)


def menu_item_detail(request, pk):
    item = get_object_or_404(MenuItem.objects.select_related('category'), pk=pk)
    return render(request, 'menu/menu_item_detail.html', {'item': item})
