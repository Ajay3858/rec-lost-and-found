from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.core.mail import send_mail
from django.conf import settings
from .otp import generate_otp

from django.http import HttpResponse

def register(request):
    if request.method == "POST":
        try:
            form = RegisterForm(request.POST)

            if not form.is_valid():
                return HttpResponse(f"<h2>Form Errors</h2><pre>{form.errors}</pre>")

            otp = generate_otp()

            request.session["otp"] = otp

            request.session["registration_data"] = {
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password1"],
            }

            send_mail(
                subject="REC Lost & Found OTP",
                message=f"Your OTP is {otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[form.cleaned_data["email"]],
                fail_silently=False,
            )

            return redirect("verify_otp")

        except Exception as e:
            return HttpResponse(f"<h1>ERROR</h1><pre>{e}</pre>")

    form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})
def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                return redirect("home")

    else:

        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):

    logout(request)

    return redirect("login")
def verify_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        saved_otp = request.session.get("otp")

        if entered_otp == saved_otp:

            data = request.session.get("registration_data")

            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"]
            )

            login(request, user)

            request.session.pop("otp", None)
            request.session.pop("registration_data", None)

            messages.success(request, "Account created successfully!")

            return redirect("home")

        else:

            messages.error(request, "Invalid OTP")

    return render(request, "accounts/verify_otp.html")