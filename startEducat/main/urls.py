from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('cpus/', views.Cpus.as_view(), name='cpus'),
    re_path(r'^cpu/(?P<pk>.*)$', views.CpuDetailView.as_view(), name='cpu-detail'),
    re_path(r'^cpumanufac/(?P<pk>.*)$', views.CpumanufacDetailView.as_view(), name='cpumanufac-detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

