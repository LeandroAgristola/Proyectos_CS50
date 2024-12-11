from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import contactForm, DevelopmentForm
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
        'developments': developments, 
        'myform': forms_contact
    })

@login_required(login_url='login')
def management(request):
    developments = development.objects.all()
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            ids_to_delete = request.POST.getlist('development_ids')

            for dev_id in ids_to_delete:
                obj = get_object_or_404(development, id=dev_id)
                obj.delete() 
            
            return redirect('management')
    
    return render(request, 'realestate/management.html', {
        'developments': developments
    })

@login_required(login_url='login')
def add_development_view(request):
    if request.method == 'POST':
        form = DevelopmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management')
    else:
        form = DevelopmentForm()
    return render(request, 'realestate/add_development.html', {'form': form})

@login_required(login_url='login')
def edit_development(request, dev_id):
    dev = get_object_or_404(development, id=dev_id)

    if request.method == 'POST':
        form = DevelopmentForm(request.POST, request.FILES, instance=dev)
        if form.is_valid():
            form.save()
            return redirect('management')
    else:
        form = DevelopmentForm(instance=dev)

    return render(request, 'realestate/edit_development.html', {'form': form, 'development': dev})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("management"))
        else:
            return render(request, "realestate/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "realestate/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))
        
def mobiledDwelling(request):
    return render(request, 'realestate/mobiledDwelling.html')

def mobileBuildings(request):
    return render(request, 'realestate/mobileBuildings.html')

def mobileIndustries(request):
    return render(request, 'realestate/mobileIndustries.html')