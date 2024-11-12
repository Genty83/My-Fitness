from django.shortcuts import render
from .models import ProductReview
from .forms import ProductReviewForm

# Create your views here.
def all_reviews(request):
    """
    View to display all product reviews.
    
    Args:
        request (HttpRequest): The request object used to generate this view.
        
    Returns:
        HttpResponse: The HTTP response to the request.
    """
    reviews = ProductReview.objects.all()
    template = 'reviews/all_reviews.html'
    context = {'reviews': reviews}
    return render(request, template, context)


def add_review(request):
    """
    View to add a new product review.
    
    Args:
        request (HttpRequest): The request object used to generate this view.
        
    Returns:
        HttpResponse: The HTTP response to the request.
    """
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProductReviewForm()
    template = 'reviews/add_review.html'
    context = {'form': form}
    return render(request, template, context)