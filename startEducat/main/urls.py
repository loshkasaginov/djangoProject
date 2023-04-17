from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.Products.as_view(), name='products'),
    re_path(r'^product/(?P<pk>.*)$', views.ProductDetailView.as_view(), name='product-detail'),
    re_path(r'^product_manufacturer/(?P<pk>.*)$', views.ProductManufacturerDetailView.as_view(),
            name='product_manufacturer-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
