from django.shortcuts import render
from .models import Product, Product_manufacturer
from django.views import generic
from django.db.models import Q


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
