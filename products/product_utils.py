from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect, reverse
from .models import Category, SubCategory, Product
import logging

logger = logging.getLogger(__name__)

def search_products(request, products):
    """
    Search for products by name or description.

    Args:
        request (HttpRequest): The HTTP request object.
        products (QuerySet): The initial queryset of products.

    Returns:
        QuerySet: The filtered queryset of products based on the search query.
    """
    query = request.GET.get('q')
    if query:
        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)
    else:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('products'))
    return products

def sort_products(request, products):
    """
    Sort products in ascending or descending order by either price or name.

    Args:
        request (HttpRequest): The HTTP request object.
        products (QuerySet): The initial queryset of products.

    Returns:
        QuerySet: The sorted queryset of products.
    """
    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name_asc': 'name',
        'name_desc': '-name',
    }
    sortkey = request.GET.get('sort')
    if sortkey in sort_options:
        products = products.order_by(sort_options[sortkey])
    return products

def filter_products(request, products):
    """
    Filter products by category and subcategory.

    Args:
        request (HttpRequest): The HTTP request object.
        products (QuerySet): The initial queryset of products.

    Returns:
        QuerySet: The filtered queryset of products.
    """
    try:
        category_id = request.GET.get('category')
        subcategory_id = request.GET.get('subcategory')
        if category_id:
            products = products.filter(category_id=category_id)
        if subcategory_id:
            products = products.filter(subcategory_id=subcategory_id)
    except Exception as e:
        logger.error("Error filtering products: %s", e)
    return products

def paginate_products(request, products, num=6):
    """
    Paginate the products list.

    Args:
        request (HttpRequest): The HTTP request object.
        products (QuerySet): The initial queryset of products.
        num (int, optional): Number of items per page. Defaults to 6.

    Returns:
        Page: The paginated page of products.
    """
    num = max(1, num)  # Ensures at least 1 item per page
    paginator = Paginator(products, num)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        logger.warning("PageNotAnInteger: Returning the first page.")
        products = paginator.page(1)
    except EmptyPage:
        logger.warning("EmptyPage: Returning the last page.")
        products = paginator.page(paginator.num_pages)
    except Exception as e:
        logger.error("Unexpected error during pagination: %s", e)
        products = paginator.page(1)
    return products

def get_items_per_category(products):
    """
    Get the total items in each category.

    Args:
        products (QuerySet): The initial queryset of products.

    Returns:
        dict: A dictionary with category names as keys and item counts as values.
    """
    categories = Category.objects.all()
    items_per_category = {
        category.name: products.filter(category_id=category.id).count()
        for category in categories
    }
    return items_per_category

def get_items_per_subcategory(products):
    """
    Get the total items in each subcategory.

    Args:
        products (QuerySet): The initial queryset of products.

    Returns:
        dict: A dictionary with subcategory names as keys and item counts as values.
    """
    subcategories = SubCategory.objects.all()
    items_per_subcategory = {
        subcategory.name: products.filter(subcategory_id=subcategory.id).count()
        for subcategory in subcategories
    }
    return items_per_subcategory
