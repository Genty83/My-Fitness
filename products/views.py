from django.contrib import messages
from django.shortcuts import redirect, reverse, render
from .models import Product, Category, SubCategory
from .product_utils import (
    search_products, sort_products, filter_products, paginate_products,
    get_items_per_category, get_items_per_subcategory
    )
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from reviews.models import ProductReview


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# Create your views here.
def all_products(request):
    """
    View to display all products with optional search, sort, and filter functionality.
    
    Retrieves all sub-categories and products. Applies search, sort, and filter 
    operations based on GET parameters. Paginates the products list based on 
    the 'items_per_page' parameter from the GET request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'all_products.html' template with the context 
        containing products, categories, sub-categories, and items per category/subcategory.
    """
    products = Product.objects.all()
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()

    if request.GET:
        products = search_products(request, products)
        products = sort_products(request, products)
        products = filter_products(request, products)

    items_per_page = 6
    # Update items per page if user selects a different value
    if request.GET.get('items_per_page'):
        items_per_page = request.GET.get('items_per_page')

    products = paginate_products(request, products, items_per_page)

    # Get avg rating using the get_average_rating function
    for product in products:
        product.rating = ProductReview.get_average_rating(product)

    context = {
        'products':  products,
        'categories': categories,
        'sub_categories': sub_categories,
        'items_per_category': get_items_per_category(Product.objects.all()),
        'items_per_subcategory': get_items_per_subcategory(Product.objects.all())
    }

    return render(request, 'products/all_products.html', context)


def product_detail(request, product_id):
    """
    View to display the details of a single product.
    
    Retrieves the product based on the provided product_id and renders the 
    'product_detail.html' template with the product context.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to be retrieved.

    Returns:
        HttpResponse: The rendered 'product_detail.html' template with the context 
        containing the product.
    """
    product = Product.objects.get(pk=product_id)
    related_products = Product.objects.filter(
        category_id=product.category_id).exclude(id=product.id).order_by('?')[:4]

    reviews = ProductReview.objects.filter(product=product)
    # Calculate the stars and half stars for the rating
    product.rating = ProductReview.get_average_rating(product)
    stars = int(product.rating)
    half_stars = 1 if product.rating % 1 >= 0.5 else 0

    template = 'products/product_detail.html'
    context = {
        'product': product,
        'reviews': reviews,
        'stars': range(stars),
        'half_stars': half_stars,
        'categories': Category.objects.all(),
        'categories': Category.objects.all(),
        'sub_categories': SubCategory.objects.all(),
        'related_products': related_products,

    }
    return render(request, template, context)


@login_required
def add_product(request):
    """
    View to add a new product to the database.
    
    Renders the 'add_product.html' template with the form to add a new product.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'add_product.html' template.
    """

    # If the form is submitted save the product to the database
    # and redirect to the product detail page showing a success message
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added successfully!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()


    context = {
        'categories': Category.objects.all(),
        'sub_categories': SubCategory.objects.all(),
        'form': form,
    }

    template = 'products/add_product.html'
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    View to edit an existing product in the database.
    
    Retrieves the product based on the provided product_id and renders the 
    'edit_product.html' template with the product context.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to be retrieved.

    Returns:
        HttpResponse: The rendered 'edit_product.html' template with the context 
        containing the product.
    """

    # If the form is submitted save the product to the database
    # and redirect to the product detail page showing a success message
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')
    
    context = {
        'form': form,
        'product': product,
        'categories': Category.objects.all(),
        'sub_categories': SubCategory.objects.all(),
    }

    template = 'products/edit_product.html'

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """
    View to delete an existing product from the database.
    
    Retrieves the product based on the provided product_id and renders the 
    'delete_product.html' template with the product context.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to be retrieved.

    Returns:
        HttpResponse: The rendered 'delete_product.html' template with the context 
        containing the product.
    """

    # Add a confirmation message before deleting the product
    # and redirect to the all products page showing a success message
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect(reverse('all_products'))

    product = Product.objects.get(pk=product_id)
    return render(request, 'products/delete_product.html', {'product': product})


def sale_products(request):
    """
    View to display all products on sale.
    
    Retrieves all products that have a discount applied and renders the 
    'sale_products.html' template with the products context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'sale_products.html' template with the context 
        containing products.
    """
    products = Product.objects.filter(discount_price__isnull=False)
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()

    if request.GET:
        products = search_products(request, products)
        products = sort_products(request, products)
        products = filter_products(request, products)

    items_per_page = 6
    # Update items per page if user selects a different value
    if request.GET.get('items_per_page'):
        items_per_page = request.GET.get('items_per_page')

    products = paginate_products(request, products, items_per_page)

    context = {
        'products':  products,
        'categories': categories,
        'sub_categories': sub_categories,
        'items_per_category': get_items_per_category(Product.objects.all()),
        'items_per_subcategory': get_items_per_subcategory(Product.objects.all())
    }

    context = {
        'products': products,
    }
    return render(request, 'products/sale_products.html', context)