from django.shortcuts import redirect, render
from django.urls import reverse

from menu.models import MenuItem

from .forms import ContactForm


def home(request):
    featured_items = MenuItem.objects.filter(is_featured=True).select_related('category')[:6]
    return render(request, 'pages/home.html', {'featured_items': featured_items})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('contact')}?sent=1")
    else:
        form = ContactForm()

    context = {
        'form': form,
        'sent': request.GET.get('sent') == '1',
    }
    return render(request, 'pages/contact.html', context)
