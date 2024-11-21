"""
This module handles the views related to product management in an e-commerce
application.

The views included are:
- Displaying all products with optional search, sort, and filter functionality.
- Displaying the details of a single product.
- Adding a new product to the database.
- Editing an existing product in the database.
- Deleting an existing product from the database.
- Displaying all products on sale.

The module also includes a custom template filter for retrieving dictionary items.
Logging and error handling have been added to ensure smooth operation and debugging.
"""

import logging
from django.contrib import messages
from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from .models import Product, Category, SubCategory
from .product_utils import (
    search_products, sort_products, filter_products, paginate_products,
    get_items_per_category, get_items_per_subcategory
)
from .forms import ProductForm
from reviews.models import ProductReview

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def all_products(request):
    """
    View to display all products with optional search, sort, and filter functionality.
    """
    try:
        products = Product.objects.all()
        categories = Category.objects.all()
        sub_categories = SubCategory.objects.all()

        if request.GET:
            products = search_products(request, products)
            products = sort_products(request, products)
            products = filter_products(request, products)

        items_per_page = request.GET.get('items_per_page', 6)

        items_per_category = get_items_per_category(products)
        items_per_subcategory = get_items_per_subcategory(products)
        products = paginate_products(request, products, items_per_page)

        for product in products:
            product.rating = ProductReview.get_average_rating(product)

        context = {
            'products': products,
            'categories': categories,
            'sub_categories': sub_categories,
            'items_per_category': items_per_category,
            'items_per_subcategory': items_per_subcategory,
        }

        logging.info("All products retrieved successfully.")
        return render(request, 'products/all_products.html', context)

    except Exception as e:
        logging.error(f"Error retrieving all products: {e}")
        messages.error(request, "An error occurred while retrieving products.")
        return redirect(reverse('home'))


def product_detail(request, product_id):
    """
    View to display the details of a single product.
    """
    try:
        product = get_object_or_404(Product, pk=product_id)
        reviews = ProductReview.objects.filter(product=product)
        for review in reviews:
            review.stars = range(int(review.rating))
            review.half_star = (review.rating % 1 != 0)

        related_products = Product.objects.filter(
            category_id=product.category_id).exclude(id=product.id).order_by('?')[:4]

        context = {
            'product': product,
            'reviews': reviews,
            'categories': Category.objects.all(),
            'sub_categories': SubCategory.objects.all(),
            'related_products': related_products,
        }

        logging.info(f"Product detail for product_id {product_id} "
                        "retrieved successfully.")
        return render(request, 'products/product_detail.html', context)

    except Exception as e:
        logging.error(f"Error retrieving product details for product_id "
                        f"{product_id}: {e}")
        messages.error(request, "An error occurred while retrieving the product "
                                "details.")
        return redirect(reverse('home'))


@login_required
def add_product(request):
    """
    View to add a new product to the database.
    """
    try:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save()
                messages.success(request, 'Product added successfully!')
                logging.info(f"Product {product.id} added successfully.")
                return redirect(reverse('product_detail', args=[product.id]))
            else:
                messages.error(request, 'Failed to add product. Please ensure '
                                        'the form is valid.')
                logging.warning("Product form is invalid.")
        else:
            form = ProductForm()

        context = {
            'categories': Category.objects.all(),
            'sub_categories': SubCategory.objects.all(),
            'form': form,
        }

        return render(request, 'products/add_product.html', context)

    except Exception as e:
        logging.error(f"Error adding product: {e}")
        messages.error(request, "An error occurred while adding the product.")
        return redirect(reverse('home'))


@login_required
def edit_product(request, product_id):
    """
    View to edit an existing product in the database.
    """
    try:
        product = get_object_or_404(Product, pk=product_id)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product updated successfully!')
                logging.info(f"Product {product.id} updated successfully.")
                return redirect(reverse('product_detail', args=[product.id]))
            else:
                messages.error(request, 'Failed to update product. Please '
                                        'ensure the form is valid.')
                logging.warning("Product form is invalid.")
        else:
            form = ProductForm(instance=product)
            messages.info(request, f'You are editing {product.name}')

        context = {
            'form': form,
            'product': product,
            'categories': Category.objects.all(),
            'sub_categories': SubCategory.objects.all(),
        }

        return render(request, 'products/edit_product.html', context)

    except Exception as e:
        logging.error(f"Error editing product {product_id}: {e}")
        messages.error(request, "An error occurred while editing the product.")
        return redirect(reverse('home'))


@login_required
def delete_product(request, product_id):
    """
    View to delete an existing product from the database.
    """
    try:
        if request.method == 'POST':
            product = get_object_or_404(Product, pk=product_id)
            product.delete()
            messages.success(request, 'Product deleted successfully!')
            logging.info(f"Product {product_id} deleted successfully.")
            return redirect(reverse('all_products'))

        product = get_object_or_404(Product, pk=product_id)
        return render(request, 'products/delete_product.html', {'product': product})

    except Exception as e:
        logging.error(f"Error deleting product {product_id}: {e}")
        messages.error(request, "An error occurred while deleting the product.")
        return redirect(reverse('home'))


def sale_products(request):
    """
    View to display all products on sale.
    """
    try:
        products = Product.objects.filter(discount_price__isnull=False)
        categories = Category.objects.all()
        sub_categories = SubCategory.objects.all()

        if request.GET:
            products = search_products(request, products)
            products = sort_products(request, products)
            products = filter_products(request, products)

        items_per_page = request.GET.get('items_per_page', 6)

        items_per_category = get_items_per_category(products)
        items_per_subcategory = get_items_per_subcategory(products)
        products = paginate_products(request, products, items_per_page)

        for product in products:
            product.rating = ProductReview.get_average_rating(product)

        context = {
            'products': products,
            'categories': categories,
            'sub_categories': sub_categories,
            'items_per_category': items_per_category,
            'items_per_subcategory': items_per_subcategory,
        }

        logging.info("Sale products retrieved successfully.")
        return render(request, 'products/sale_products.html', context)

    except Exception as e:
        logging.error(f"Error retrieving sale products: {e}")
        messages.error(request, "An error occurred while retrieving sale products.")
        return redirect(reverse('home'))
