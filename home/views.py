from django.shortcuts import render


def home(request):
    '''
    Render the homepage template.
    '''
    return render(request, 'home/home.html')
