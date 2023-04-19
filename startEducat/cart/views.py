from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product
from .models import CartItem
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    previous_page = request.META.get('HTTP_REFERER', reverse_lazy('index'))
    return redirect(previous_page)


@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item = get_object_or_404(CartItem, user=request.user, product=product)
    cart_item.quantity -= 1
    if cart_item.quantity <= 0:
        cart_item.delete()
    else:
        cart_item.save()
    return redirect('cart')


@login_required
def clear_cart(request):
    CartItem.objects.filter(user=request.user).delete()
    return redirect('cart')


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'cart_total': cart_total})
