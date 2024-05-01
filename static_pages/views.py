from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail
from django.shortcuts import redirect

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

def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            send_mail(
                subject=f'Message from {name}',
                message=message,
                from_email=email,
                recipient_list=['vaultewestminster@gmail.com'],
            )
            return redirect('contactus')  # Redirect after POST
    else:
        form = ContactForm()

    return render(request, 'contactus.html', {'form': form})