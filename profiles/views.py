from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order


def profile(request):
    """
    Display the user's profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the rendered profile page.
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    Display the order history.

    Args:
        request (HttpRequest): The HTTP request object.
        order_number (str): The order number to fetch.

    Returns:
        HttpResponse: The HTTP response with the rendered order history page.
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
