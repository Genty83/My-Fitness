from django.shortcuts import render

# Create your views here.
def bag(request):

    context = {
        
    }   
    return render(request, 'bag/bag.html', context)