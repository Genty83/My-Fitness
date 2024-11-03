from django.shortcuts import render

# Create your views here.
def favourites(request):

    context = {
        
    }   
    return render(request, 'favourites/favourites.html', context)