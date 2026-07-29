from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import ItemForm
from .models import Item

def home(request):

    recent_items = Item.objects.order_by("-created_at")[:6]

    context = {
        "recent_items": recent_items,
        "lost_count": Item.objects.filter(status="Lost").count(),
        "found_count": Item.objects.filter(status="Found").count(),
        "recovered_count": 0,  # Update later when adding recovery feature
        "today_count": Item.objects.filter(
            created_at__date=timezone.now().date()
        ).count(),
    }

    return render(request, "home.html", context)
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def report_lost(request):

    if request.method == "POST":

        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():

            item = form.save(commit=False)

            item.user = request.user

            item.status = "Lost"

            item.save()

            return redirect("lost_items")

    else:

        form = ItemForm()

    return render(request,
                  "report_lost.html",
                  {"form": form})

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def report_found(request):

    if request.method == "POST":

        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():

            item = form.save(commit=False)

            item.user = request.user

            item.status = "Found"

            item.save()

            return redirect("found_items")

    else:

        form = ItemForm()

    return render(request, "report_found.html", {"form": form})
from django.db.models import Q

def lost_items(request):

    query = request.GET.get("q", "")

    items = Item.objects.filter(status="Lost")

    if query:

        items = items.filter(

            Q(item_name__icontains=query) |
            Q(category__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)

        )

    items = items.order_by("-created_at")

    return render(
        request,
        "lost_items.html",
        {
            "items": items,
            "query": query,
        }
    )
def found_items(request):

    query = request.GET.get("q", "")

    items = Item.objects.filter(status="Found")

    if query:

        items = items.filter(

            Q(item_name__icontains=query) |
            Q(category__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)

        )

    items = items.order_by("-created_at")

    return render(
        request,
        "found_items.html",
        {
            "items": items,
            "query": query,
        }
    )
from django.contrib.auth.decorators import login_required
@login_required
def profile(request):
    return render(request, "profile.html")
@login_required
def dashboard(request):
    return render(request, "dashboard.html")