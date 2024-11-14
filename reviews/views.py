from django.shortcuts import render, redirect
from .models import ProductReview
from .forms import ProductReviewForm
from products.models import Product
from django.contrib import messages

# Create your views here.
def all_reviews(request, product_id):
    """
    View to display all reviews for a specific product.
    
    Args:
        request (HttpRequest): The request object used to generate this view.
        product_id (int): The ID of the product being reviewed.
        
    Returns:
        HttpResponse: The HTTP response to the request.
    """
    product = Product.objects.get(id=product_id)
    reviews = ProductReview.objects.filter(product=product)
    
    # Get the stars for all reviews
    for review in reviews:
        review.stars = range(int(review.rating))
        if review.rating - int(review.rating) > 0:
            review.half_star = True
    
    template = 'reviews/all_reviews.html'
    context = {'product': product, 'reviews': reviews}
    return render(request, template, context)

def add_review(request, product_id):
    """
    View to add a new product review.
    
    Args:
        request (HttpRequest): The request object used to generate this view.
        product_id (int): The ID of the product being reviewed.
        
    Returns:
        HttpResponse: The HTTP response to the request.
    """
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.username = request.user
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('product_detail', product_id=product_id)
        else:
            messages.error(request, 
                'There was an error submitting your review. Please try again.')
    else:
        form = ProductReviewForm()
        
    template = 'reviews/add_review.html'
    context = {'form': form, 'product': product}
    return render(request, template, context)

def edit_review(request, review_id):
    """
    View to edit an existing product review.
    
    Args:
        request (HttpRequest): The request object used to generate this view.
        review_id (int): The ID of the review being edited.
        
    Returns:
        HttpResponse: The HTTP response to the request.
    """
    review = ProductReview.objects.get(id=review_id)
    product = review.product
    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated.')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 
                'There was an error updating your review. Please try again.')
    else:
        form = ProductReviewForm(instance=review)
        
    template = 'reviews/edit_review.html'
    context = {'form': form, 'product': product, 'review': review}
    return render(request, template, context)


def delete_review(request, review_id):
    """
    View to delete an existing product review.
    
    Args:
        request (HttpRequest): The request object used to generate this view.
        review_id (int): The ID of the review being deleted.
        
    Returns:
        HttpResponse: The HTTP response to the request.
    """
    review = ProductReview.objects.get(id=review_id)

    if request.user == review.username:
        review.delete()
        messages.success(request, 'Your review has been deleted.')
        redirect('product_detail', product_id=review.product.id)    
        
    template = 'reviews/delete_review.html'
    context = {
        "product_id": review.product.id
        }
    return render(request, template, context)
