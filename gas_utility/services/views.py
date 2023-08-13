from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .models import ServiceRequest
from .forms import ServiceRequestForm, ServiceRequestUpdateForm, UserRegistrationForm
from django.contrib.auth.decorators import user_passes_test

def staff_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return redirect('service_request')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def login(request):
    return auth_views.LoginView.as_view(template_name='registration/login.html')(request)

def login(request):
    if request.method == 'POST':
        # Attempt to log the user in
        response = auth_views.LoginView.as_view(template_name='registration/login.html')(request)
        
        # Check if the login was successful
        if request.user.is_authenticated:
            # Redirect to the service_request page
            return redirect('service_request')
        else:
            return response
    else:
        return auth_views.LoginView.as_view(template_name='registration/login.html')(request)

def logout(request):
    return auth_views.LogoutView.as_view(template_name='registration/logout.html')(request)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            return redirect('request_tracking')
    else:
        form = ServiceRequestForm()
    return render(request, 'service_requests/service_request.html', {'form': form})

@login_required
def request_tracking(request):
    service_requests = ServiceRequest.objects.filter(customer=request.user).order_by('-date_submitted')
    return render(request, 'service_requests/request_tracking.html', {'service_requests': service_requests})

@login_required
@staff_required
def manage_requests(request):
    if request.method == 'POST':
        form = ServiceRequestUpdateForm(request.POST)
        if form.is_valid():
            service_request_id = request.POST.get('service_request_id')
            service_request = ServiceRequest.objects.get(id=service_request_id)
            service_request.status = form.cleaned_data['status']
            service_request.save()
            return redirect('manage_requests')
    else:
        form = ServiceRequestUpdateForm()
    service_requests = ServiceRequest.objects.all().order_by('-date_submitted')
    return render(request, 'service_requests/manage_requests.html', {'service_requests': service_requests, 'form': form})


