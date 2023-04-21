from django.db.models import Q
from django.http import JsonResponse

from .models import Profile
from django.views import generic
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserForm, ProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from .models import Product, Product_manufacturer, PurchasedProduct
from .forms import OrderForm


def ProductManufacturerDetailView(request):
    return render(request, 'main/about.html', )


def index(request):
    products = Product.objects.all()[:5]
    return render(request, 'main/index.html', {'products': products})


def product_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(product_name__icontains=search_query)
    else:
        products = Product.objects.all()
    return render(request, 'main/products.html', {'products': products, 'search_query': search_query})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'main/product-detail.html', {'product': product})



def about(request):
    return render(request, 'main/about.html', )


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт для {username} был успешно создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    if not hasattr(request.user, 'profile'):
        Profile.create_profile(request.user)

    profile = request.user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        password_change_form = PasswordChangeForm(request.user, request.POST)

        if 'password1' in request.POST:
            if password_change_form.is_valid():
                user = password_change_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно изменен!')
                return redirect('profile')
        else:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Данные профиля успешно изменены!')
                return redirect('profile')

    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    password_change_form = PasswordChangeForm(request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_change_form': password_change_form,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect(product.get_absolute_url())
    else:
        form = ReviewForm()
    return render(request, 'main/add_review.html', {'form': form, 'product': product})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            # Здесь мы добавляем товары из корзины в таблицу PurchasedProduct и удаляем их из таблицы Product
            cart_items = request.session.get('cart', {})
            for product_id, quantity in cart_items.items():
                product = Product.objects.get(pk=product_id)
                for _ in range(quantity):
                    PurchasedProduct.objects.create(user=request.user if request.user.is_authenticated else None,
                                                    product=product)
                    product.delete()

            # Очищаем корзину
            request.session['cart'] = {}

            messages.success(request, 'Заказ успешно оформлен!')
            return redirect('index')
    else:
        if request.user.is_authenticated:
            initial_data = {
                'country': request.user.profile.country,
                'city': request.user.profile.city,
                'email': request.user.email,
            }
            form = OrderForm(initial=initial_data)
        else:
            form = OrderForm()

    return render(request, 'main/create_order.html', {'form': form})


class Products(generic.ListView):
    model = Product
    template_name = 'main/products.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = Product.objects.filter(
                Q(product_name__icontains=search_query)
            )
        else:
            queryset = Product.objects.all()
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product = self.object

        # Check if the request is for adding a product to the cart
        if 'quantity' in request.POST:
            quantity = int(request.POST.get('quantity'))
            if quantity <= product.quantity:
                cart = request.session.get('cart', {})
                cart[str(product.pk)] = cart.get(str(product.pk), 0) + quantity
                request.session['cart'] = cart
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Товара недостаточно на складе"})
        else:
            # ... Handle other types of POST requests here
            return JsonResponse({"success": False, "error": "Неизвестный тип запроса"})





@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
    return redirect('product-detail', pk=product.pk)
