"""views.py"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import NewUserForm
from .models import Menu

# Create your views here.


def register_request(request):
    """register request"""
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Congratulations! You have successfully registered."
            )
            return redirect("home")
        messages.error(
            request, "Unsuccessful registration. Please follow the instructions."
        )
    form = NewUserForm()
    return render(
        request=request, template_name="register.html", context={"register_form": form}
    )


def login_request(request):
    """login request"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="login.html", context={"login_form": form}
    )


def logout_request(request):
    """logout request"""
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


# Create your views here.


def menu(request):
    """menu page"""
    context = {}
    if request.user.is_authenticated:
        context["p"] = "Logout"
    else:
        context["p"] = "Sign-in"
    data = Menu.objects.all().order_by("-id")
    context["data"] = data
    return render(request, "menu.html", context)


def index(request):
    """index page"""
    if request.user.is_authenticated:
        context = {"data": "Logout"}
    else:
        context = {"data": "Sign-in"}
    return render(request, "index.html", context)


def about(request):
    """about page"""
    if request.user.is_authenticated:
        context = {"data": "Logout"}
    else:
        context = {"data": "Sign-in"}
    return render(request, "about.html", context)
