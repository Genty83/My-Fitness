from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect, reverse
from .models import Category, SubCategory, Product


def search_products(request, products):
    """
    Search for products by name or description.

    Args:
        request (HttpRequest): The HTTP request object.
        products (QuerySet): The initial queryset of products.

    Returns:
        QuerySet: The filtered queryset of products based on the search query.
    """
    query = None
    if request.GET.get('q'):
        query = request.GET.get('q')
        if not query:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('products'))

        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)
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
    if request.GET.get('sort'):
        sortkey = request.GET.get('sort')
        if sortkey == 'price_asc':
            products = products.order_by('price')
        elif sortkey == 'price_desc':
            products = products.order_by('-price')
        elif sortkey == 'name_asc':
            products = products.order_by('name')
        elif sortkey == 'name_desc':
            products = products.order_by('-name')
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
    if request.GET.get('category'):
        products = products.filter(
            category_id=request.GET.get('category'))
    if request.GET.get('subcategory'):
        products = products.filter(
            subcategory_id=request.GET.get('subcategory'))
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
    paginator = Paginator(products, num)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
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
    items_per_category = {}
    for category in categories:
        items_per_category[category.name] = products.filter(
            category_id=category).count()
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
    items_per_subcategory = {}
    for subcategory in subcategories:
        items_per_subcategory[subcategory.name] = products.filter(
            subcategory_id=subcategory).count()
    return items_per_subcategory
