from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def bag(request):
    """ """
    context = {
        
    }   
    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_id):
    """ """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    # Add message to confirm product added to bag
    messages.success(request, f'Added {quantity} of this product to your bag!')

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of a specific item in the shopping bag.

    Args:
        request: The HTTP request object containing POST data.
        item_id: The ID of the item to adjust in the bag.

    Returns:
        A redirect to the bag page.
    """
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
    else:
        bag.pop(item_id)

    request.session['bag'] = bag
    # Add message to confirm product quantity adjusted
    messages.success(request, f'Updated quantity of this product in your bag!')

    return redirect('bag')


def remove_from_bag(request, item_id):
    """ """
    bag = request.session.get('bag', {})

    try:
        bag.pop(item_id)
        request.session['bag'] = bag
        # Add message to confirm product removed from bag
        messages.success(request, f'Removed this product from your bag!')
        return redirect('bag')
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return redirect('bag')
