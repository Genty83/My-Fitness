from django.shortcuts import render
from newsletter.models import SubscribeToNewsletter
from products.models import Category, SubCategory


# Create your views here.
def home(request):

    # Check if the signed in user is subscribed to the newsletter
    subscribed_user = False
    
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()

    if request.user.is_authenticated:
        subscribed_user = SubscribeToNewsletter.objects.filter(
            email=request.user.email).exists()

    context = {
        'subscribed_user': subscribed_user,
        'categories': categories,
        'sub_categories': sub_categories
    }

    return render(request, 'home/home.html', context)
