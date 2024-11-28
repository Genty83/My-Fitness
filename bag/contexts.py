from django.conf import settings
from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):
    """
    Calculate the contents of the shopping bag, 
    including total cost, delivery charge,
    and grand total, and return the context dictionary for use in templates.

    Args:
        request: The HTTP request object containing session data.

    Returns:
        A dictionary containing the bag contents, total cost, product count,
        delivery charge, amount needed to qualify for free delivery, free delivery threshold,
        grand total, and individual bag items with their details.
    """

    bag_items = []
    total = 0
    sub_total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        if product.discount_price is None:
            total += quantity * product.price
            sub_total = product.price * quantity
        else:
            total += quantity * product.discount_price
            sub_total = product.discount_price * quantity

        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
            'sub_total': sub_total
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'bag_items': bag_items,
    }

    return context
