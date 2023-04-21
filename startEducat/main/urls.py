from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from .views import profile
from .views import add_review

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('create_order/', views.create_order, name='create_order'),
    path('products/', views.Products.as_view(), name='products'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('product/<int:pk>/add_review/', add_review, name='add_review'),
    re_path(r'^product/(?P<pk>.*)$', views.ProductDetailView.as_view(), name='product-detail'),
    re_path(r'^product_manufacturer/(?P<pk>.*)$', views.ProductManufacturerDetailView,
            name='product_manufacturer-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

