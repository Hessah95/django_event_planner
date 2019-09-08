from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, CreatForm
from django.contrib import messages
from .models import Event
from datetime import datetime

def home(request):
    if request.user.is_anonymous :
        return redirect ("login")

    context = {
        'event' : Event.objects.filter(date__gt=datetime.now()),
    }
    return render(request, 'home.html', context)

def dashboard(request):
    if request.user.is_anonymous :
        return redirect ("login")

    context = {
        'event' : Event.objects.filter(owner=request.user),
    }

    return render(request, 'dashboard.html', context)


def create(request):
    if request.user.is_anonymous :
        return redirect ('login')
    form = CreatForm()
    if request.method == "POST" :
        form = CreatForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            return redirect ('dashboard')
    context = {
        'form' : form,
    }
    return render (request, 'create.html', context)



class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('home')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")



def detail (request, event_id) :
    event = Event.objects.get(id=event_id)
    context = {
    'event': event,
    }
    return render(request, 'detail.html', context)
    