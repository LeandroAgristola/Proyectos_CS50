from django.shortcuts import render
from django.http import JsonResponse
from .forms import contactForm
from django.core.mail import EmailMessage
from .models import development

def home(request):
    developments = development.objects.all()

    if request.method == "POST":
        contact_Form = contactForm(data=request.POST)
        if contact_Form.is_valid():
            name = contact_Form.cleaned_data['name']
            lastname = contact_Form.cleaned_data['apellido']
            phonenumber = contact_Form.cleaned_data['phonenumber']
            email = contact_Form.cleaned_data['email']
            consultation = contact_Form.cleaned_data['onsultation']

            email_message = EmailMessage(
                "Message from Django App Real Estate",
                f"Name: {name} {lastname}\nPhonenumber: {phonenumber}\nEmail: {email}\nConsultation: {consultation}",
                "", 
                [""], 
                reply_to=[email]
            )

            try:
                email_message.send()
                return JsonResponse({'status': 'ok'}, status=200)
            except Exception as e:
                print(f"Error sending email: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            errores = contact_Form.errors.as_json()
            return JsonResponse({'status': 'invalid', 'errors': errores}, status=400)
    
    contact_Form = contactForm()
    return render(request, 'realestate/home.html', {
        'development': developments, 
        'myform': contact_Form
    })

def mobiledDwelling(request):
    return render(request, 'realestate/mobiledDwelling.html')

def mobileBuildings(request):
    return render(request, 'realestateapp/mobileBuildings.html')

def mobileIndustries(request):
    return render(request, 'realestateapp/mobileIndustries.html')