from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .forms import DestinationForm, PointOfInterestForm, RegisterForm, UserUpdateForm
from .models import Bookmark, Category, Destination, PointsOfInterest, Visited


# ==========================================
#  Views Προορισμών
# ==========================================

def home_view(request):
    """View για την Αρχική Σελίδα με Αναζήτηση & Φιλτράρισμα"""
    destinations = Destination.objects.all()
    categories = Category.objects.all()

    # 1. Λήψη παραμέτρων από το URL (request.GET)
    query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()

    # 2. Φιλτράρισμα με βάση το κείμενο αναζήτησης (Τίτλος, Χώρα, Περιγραφή)
    if query:
        destinations = destinations.filter(
            Q(title__icontains=query)
            | Q(country__icontains=query)
            | Q(description__icontains=query)
        )

    # 3. Φιλτράρισμα με βάση την κατηγορία (μέσω των POIs)
    if selected_category:
        destinations = destinations.filter(pois__categories__id=selected_category).distinct()

    # 4. Λήψη bookmarks & visited για τον συνδεδεμένο χρήστη (για τα εικονίδια)
    if request.user.is_authenticated:
        user_bookmarks = Bookmark.objects.filter(user=request.user).values_list('destination_id', flat=True)
        user_visited = Visited.objects.filter(user=request.user).values_list('destination_id', flat=True)
    else:
        user_bookmarks = []
        user_visited = []

    context = {
        "destinations": destinations,
        "categories": categories,
        "query": query,
        "selected_category": selected_category,
        "user_bookmarks": user_bookmarks,
        "user_visited": user_visited,
    }

    return render(request, "destinations/home.html", context)


def destination_detail_view(request, slug):
    """View για τη σελίδα λεπτομερειών ενός συγκεκριμένου προορισμού"""
    destination = get_object_or_404(Destination, slug=slug)
    pois = destination.pois.all()

    context = {
        "destination": destination,
        "pois": pois,
    }

    return render(request, "destinations/destination_detail.html", context)


# ==========================================
# Πιστοποίηση Χρηστών
# ==========================================

def register_view(request):
    """View για την Εγγραφή νέου χρήστη"""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Αυτόματη σύνδεση μετά την εγγραφή
            messages.success(request, f"Καλώς ήρθες, {user.username}! Η εγγραφή ολοκληρώθηκε.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "destinations/register.html", {"form": form})


def login_view(request):
    """View για τη Σύνδεση χρήστη"""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Συνδέθηκες ως {username}.")
                return redirect("home")
        messages.error(request, "Λάθος όνομα χρήστη ή κωδικός.")
    else:
        form = AuthenticationForm()

    # Προσθήκη Bootstrap class στα πεδία της έτοιμης φόρμας
    for field_name, field in form.fields.items():
        field.widget.attrs["class"] = "form-control"

    return render(request, "destinations/login.html", {"form": form})


def logout_view(request):
    """View για την Αποσύνδεση χρήστη"""
    logout(request)
    messages.info(request, "Αποσυνδεθήκατε επιτυχώς.")
    return redirect("home")


@login_required
def profile_view(request):
    """View για το Προφίλ Χρήστη"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Το προφίλ σου ενημερώθηκε με επιτυχία!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    # Παίρνουμε τις λίστες του χρήστη
    user_bookmarks = Bookmark.objects.filter(user=request.user).select_related('destination')
    user_visited = Visited.objects.filter(user=request.user).select_related('destination')

    context = {
        'form': form,
        'user_bookmarks': user_bookmarks,
        'user_visited': user_visited,
    }
    return render(request, 'destinations/profile.html', context)


@login_required
def toggle_bookmark_view(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, destination=destination)
    
    if not created:
        bookmark.delete()
        messages.info(request, f"Αφαιρέθηκε ο προορισμός {destination.title} από τα Αγαπημένα.")
    else:
        messages.success(request, f"Προστέθηκε ο προορισμός {destination.title} στα Αγαπημένα!")
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def toggle_visited_view(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    visited, created = Visited.objects.get_or_create(user=request.user, destination=destination)
    
    if not created:
        visited.delete()
        messages.info(request, f"Αφαιρέθηκε ο προορισμός {destination.title} από τα μέρη που έχεις επισκεφθεί.")
    else:
        messages.success(request, f"Σημειώθηκε ο προορισμός {destination.title} ως «Έχω πάει»!")
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ==========================================
#  Views Προσθήκης από Frontend (Forms)
# ==========================================

@login_required
def add_destination_view(request):
    """View για την προσθήκη νέου προορισμού"""
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.slug = slugify(destination.title)
            destination.save()
            messages.success(request, f'Ο προορισμός "{destination.title}" δημιουργήθηκε με επιτυχία!')
            return redirect('destination_detail', slug=destination.slug)
    else:
        form = DestinationForm()

    return render(request, 'destinations/add_destination.html', {'form': form})


@login_required
def add_poi_view(request, destination_id):
    """View για την προσθήκη νέου POI σε συγκεκριμένο προορισμό"""
    destination = get_object_or_404(Destination, id=destination_id)

    if request.method == 'POST':
        form = PointOfInterestForm(request.POST, request.FILES)
        if form.is_valid():
            poi = form.save(commit=False)
            poi.destination = destination
            poi.save()
            form.save_m2m()  # Απαραίτητο για τα ManyToMany πεδία (όπως οι κατηγορίες)
            messages.success(request, f'Το αξιοθέατο "{poi.title}" προστέθηκε στον προορισμό {destination.title}!')
            return redirect('destination_detail', slug=destination.slug)
    else:
        form = PointOfInterestForm()

    return render(
        request,
        'destinations/add_poi.html',
        {'form': form, 'destination': destination},
    )