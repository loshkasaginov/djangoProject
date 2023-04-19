from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from .models import Product, Product_manufacturer, Profile
from django.views import generic
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, login
from .forms import UserForm, ProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Review
from .forms import ReviewForm


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


class Products(generic.ListView):
    model = Product
    template_name = 'main/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = Product.objects.filter(
                Q(product_name__icontains=search_query)
            )
        else:
            queryset = Product.objects.all()
        return queryset


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'main/product-detail.html'


class ProductManufacturerDetailView(generic.DetailView):
    model = Product_manufacturer
    template_name = 'main/product_manufacturer-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        self.object = self.get_object()
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.product = self.object
            new_review.save()
            return redirect(request.path)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name, context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        context['form'] = ReviewForm()
        return context


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
