from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product
from .models import CartItem
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart_items = request.session.get('cart_items', [])
        for item in cart_items:
            if item['id'] == pk:
                item['quantity'] += 1
                break
        else:
            cart_items.append({'id': pk, 'quantity': 1, 'price': str(product.product_price)})
        request.session['cart_items'] = cart_items

    previous_page = request.META.get('HTTP_REFERER', reverse_lazy('index'))
    return redirect(previous_page)

def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product=product)
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
    else:
        cart_items = request.session.get('cart_items', [])
        for item in cart_items:
            if item['id'] == pk:
                item['quantity'] -= 1
                if item['quantity'] <= 0:
                    cart_items.remove(item)
                break
        request.session['cart_items'] = cart_items

    return redirect('cart')


def clear_cart(request):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()
    else:
        request.session['cart_items'] = []

    return redirect('cart')


def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_total = sum(item.get_total_price() for item in cart_items)
    else:
        cart_items_data = request.session.get('cart_items', [])
        cart_items = []
        cart_total = 0
        for item_data in cart_items_data:
            product = get_object_or_404(Product, pk=item_data['id'])
            quantity = item_data['quantity']
            price = Decimal(item_data['price'])
            cart_item = {
                'product': product,
                'quantity': quantity,
                'get_total_price': price * quantity,
            }
            cart_items.append(cart_item)
            cart_total += cart_item['get_total_price']

    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'cart_total': cart_total})
