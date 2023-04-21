# cart/context_processors.py
from .models import CartItem


def cart_items_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        items_count = sum(item.quantity for item in cart_items)
    else:
        items_count = sum(item['quantity'] for item in request.session.get('cart_items', []))
    return {'cart_items_count': items_count}
