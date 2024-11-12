from django.urls import path
from .views import all_reviews

urlpatterns = [
    path('', all_reviews, name='all_reviews'),
]