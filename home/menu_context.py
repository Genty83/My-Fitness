from products.models import Category, SubCategory

# This function will return the menu items getting the rel subcategories for each category     

def menu(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    
    context = {
        'menu_categories': categories,
        'menu_subcategories': subcategories,
    }
    
    return context