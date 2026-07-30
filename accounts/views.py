from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

from .forms import RegisterForm
from .otp import generate_otp


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if not form.is_valid():
            return HttpResponse(f"<h2>Form Errors</h2><pre>{form.errors}</pre>")

        try:

            otp = generate_otp()

            request.session["otp"] = otp

            request.session["registration_data"] = {
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password1"],
            }

            try:

                send_mail(
                    subject="REC Lost & Found OTP Verification",
                    message=f"Your OTP is {otp}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[form.cleaned_data["email"]],
                    fail_silently=False,
                )

            except Exception as e:

                return HttpResponse(
                    f"<h2>Email Error</h2><pre>{type(e).__name__}: {e}</pre>"
                )

            return redirect("verify_otp")

        except Exception as e:

            return HttpResponse(
                f"<h2>Registration Error</h2><pre>{type(e).__name__}: {e}</pre>"
            )

    else:

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

        messages.error(request, "Invalid username or password.")

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

            messages.success(
                request,
                "Account created successfully!"
            )

            return redirect("home")

        else:

            messages.error(request, "Invalid OTP")

    return render(request, "accounts/verify_otp.html")