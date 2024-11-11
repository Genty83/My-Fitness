from django.shortcuts import render
from newsletter.models import SubscribeToNewsletter

# Create your views here.
def home(request):

    # Check if the signed in user is subscribed to the newsletter
    subscribed_user = False

    if request.user.is_authenticated:
        subscribed_user = SubscribeToNewsletter.objects.filter(
            email=request.user.email).exists()

    context = {
        'subscribed_user': subscribed_user
    }

    return render(request, 'home/home.html', context)
