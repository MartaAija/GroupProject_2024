from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def termsnconditions(request):
    return render(request, 'termsnconditions.html')

def contactus(request):
    return render(request, 'contactus.html')

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

def history(request):
    return render(request, 'history.html')

def privacy(request):
    return render(request, 'privacy.html')