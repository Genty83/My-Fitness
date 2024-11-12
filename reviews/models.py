from django.db import models
from products.models import Product
from django.contrib.auth.models import User


# Create your models here.
class ProductReview(models.Model):
    """
    Model representing a review for a product.
    
    Attributes:
        product (ForeignKey): The product being reviewed.
        user (ForeignKey): The user who wrote the review.
        review (TextField): The text content of the review.
        rating (DecimalField): The rating given to the product.
        date (DateTimeField): The date and time when the review was created.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """
        String representation of the ProductReview model.
        
        Returns:
            str: The text content of the review.
        """
        return self.review
    

    def get_average_rating(product):
        """
        Function to calculate the average rating for a product.
        
        Args:
            product (Product): The product for which to calculate the average rating.
            
        Returns:
            Decimal: The average rating for the product.
        """
        reviews = ProductReview.objects.filter(product=product)
        if reviews:
            total_rating = sum([review.rating for review in reviews])
            average_rating = total_rating / len(reviews)
            return average_rating
        else:
            return 0
