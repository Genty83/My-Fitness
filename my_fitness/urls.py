"""
URL configuration for my_fitness project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # include the allauth urls
    path('accounts/', include('allauth.urls')),
    # include the fitness app urls
    path('', include('home.urls')),
    # include the products app urls
    path('products/', include('products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)