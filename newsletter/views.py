from django.shortcuts import render

# Create your views here.
def newsletter(request):

    context = {
        
    }   
    return render(request, 'newsletter/newsletter.html', context)