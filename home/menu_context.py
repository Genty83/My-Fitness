from products.models import Category, SubCategory
from newsletter.models import SubscribeToNewsletter

# This function will return the menu items getting the rel subcategories for each category     

def menu(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    

    if request.user.is_authenticated:
        subscribed_user = SubscribeToNewsletter.objects.filter(
            email=request.user.email).exists()
    else:
        subscribed_user = None
    
    context = {
        'menu_categories': categories,
        'menu_subcategories': subcategories,
        'subscribed_user': subscribed_user,
    }
    
    return context