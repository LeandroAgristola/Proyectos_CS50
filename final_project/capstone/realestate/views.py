from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMessage
from .forms import contactForm
from .models import development

def home(request):
    developments = development.objects.all()

    if request.method == "POST":
        forms_contact = contactForm(data=request.POST)
        if forms_contact.is_valid():
            name = forms_contact.cleaned_data['name']
            lastname = forms_contact.cleaned_data['lastname']
            phonenumber = forms_contact.cleaned_data['phonenumber']
            email = forms_contact.cleaned_data['email']
            consultation = forms_contact.cleaned_data['consultation']

            email_message = EmailMessage(
                "Message from Real Estate",
                f"Name: {name} {lastname}\nPhonenumber: {phonenumber}\nEmail: {email}\nConsultation: {consultation}",
                "#",  
                ["#"],  
                reply_to=[email]
            )

            try:
                email_message.send()
                return JsonResponse({'status': 'ok'}, status=200)
            except Exception as e:
                print(f"Error sending email: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            errors = forms_contact.errors.as_json()
            return JsonResponse({'status': 'invalid', 'errors': errors}, status=400)
    
    forms_contact = contactForm()
    return render(request, 'realestate/home.html', {
        'development': developments, 
        'myform': forms_contact
    })
        
def mobiledDwelling(request):
    return render(request, 'realestate/mobiledDwelling.html')

def mobileBuildings(request):
    return render(request, 'realestateapp/mobileBuildings.html')

def mobileIndustries(request):
    return render(request, 'realestateapp/mobileIndustries.html')