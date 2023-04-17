from django.shortcuts import render
from .models import Product, Product_manufacturer
from django.views import generic


def index(request):
    num_product = Product.objects.all().count()
    num_product_manufacturer = Product_manufacturer.objects.all().count()
    return render(request,
                  'main/index.html',
                  context={
                      'num_product': num_product, 'num_product_manufacturer': num_product_manufacturer
                  })


def about(request):
    return render(request, 'main/about.html',)


class Products(generic.ListView):
    model = Product
    # context_object_name = 'my_cpu_list'
    # queryset = CPU.objects.all()
    template_name = 'main/products.html'
    paginate_by = 10


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'main/product-detail.html'


class ProductManufacturerDetailView(generic.DetailView):
    model = Product_manufacturer
    template_name = 'main/product_manufacturer-detail.html'
