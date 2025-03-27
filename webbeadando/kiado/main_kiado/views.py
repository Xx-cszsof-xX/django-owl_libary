from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _
from .models import Book, Review, Employee, Cart, CartItem, Purchase, Profile
from .forms import ReviewForm, RegisterForm, UserProfileForm
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.http import JsonResponse
from django.views import View

# === Főoldal nézete ===
def home(request):
    books = Book.objects.all()
    employees = Employee.objects.all()
    return render(request, 'main_kiado/home.html', {'books': books, 'employees': employees})

# === "Rólunk" oldal nézete ===
def about(request):
    return render(request, 'main_kiado/about.html')

# === Munkatársak listázása ===
def employees(request):
    employees = Employee.objects.all()
    return render(request, 'main_kiado/employees.html', {'employees': employees})

# === Kapcsolat oldal nézete ===
def contact(request):
    return render(request, 'main_kiado/contact.html')

# === Könyvek listázása ===
def books(request):
    all_books = Book.objects.all()
    return render(request, 'main_kiado/books.html', {'books': all_books})

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Book.objects.filter(title__icontains=query)
    return render(request, 'main_kiado/search_results.html', {'query': query, 'results': results})
    
# === Vélemények kezelése ===
def reviews(request):
    all_reviews = Review.objects.all().order_by('-date')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Sikeresen elküldted a véleményed!'))
            return redirect('reviews')
    else:
        form = ReviewForm()

    return render(request, 'main_kiado/reviews.html', {'form': form, 'reviews': all_reviews})

# === Kosárkezelés ===
@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not item_created:
        cart_item.quantity += quantity
        messages.info(request, _("A könyv mennyisége nőtt."))
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return redirect('cart')

@login_required
def remove_from_cart(request, book_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, book_id=book_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.info(request, _("A könyv mennyisége csökkent."))
    else:
        cart_item.delete()
        messages.info(request, _("A könyvet eltávolítottad a kosárból."))

    return redirect('cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = cart.total_price()

    return render(request, 'main_kiado/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.error(request, _("A kosarad üres, nem lehet vásárlást végrehajtani."))
        return redirect('cart')

    for item in cart.items.all():
        Purchase.objects.create(
            user=request.user,
            book=item.book,
            purchased_at=timezone.now()
        )

    cart.items.all().delete()
    messages.success(request, _('Sikeresen vásároltál! Köszönjük a rendelést.'))
    
    return render(request, 'main_kiado/checkout.html')

# === Regisztráció ===
class RegisterView(View):
    form_class = RegisterForm
    template_name = 'main_kiado/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _('Sikeresen létrejött a fiók: %(username)s!') % {'username': username})
            return redirect('login')
        return render(request, self.template_name, {'form': form})

# === Profil megtekintése és szerkesztése ===
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profilod sikeresen frissítve lett."))
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'main_kiado/profile.html', {'form': form})

# === 404-es oldal ===
def custom_404_view(request, exception):
    return render(request, 'main_kiado/404.html', status=404)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.utils import timezone
from .models import Book, Purchase, Cart, CartItem, Employee, Profile
from .forms import UserProfileForm


# === Könyvvásárlás ===
@login_required
def purchase_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    Purchase.objects.create(user=request.user, book=book)
    messages.success(request, _("Sikeres vásárlás!"))
    return redirect('home')


# === Admin vásárlási lista ===
@user_passes_test(lambda u: u.is_superuser)  # Csak adminok láthatják
def admin_purchase_list(request):
    cart_items = Cart.objects.all()
    query = request.GET.get('q')
    if query:
        cart_items = cart_items.filter(user__username__icontains=query)  # Felhasználónév alapján szűrés
    return render(request, 'main_kiado/admin_purchase_list.html', {'cart_items': cart_items})


# === Vásárlási lista nézet ===
def purchase_list_view(request):
    carts = Cart.objects.all()
    return render(request, 'admin_purchase_list.html', {'cart_items': carts})


# === Profil nézet ===
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profilod sikeresen frissítve lett."))
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'main_kiado/profile.html', {'form': form})


# === Hibakezelések ===
def custom_400_view(request, exception):
    return render(request, '400.html', status=400)


def custom_403_view(request, exception):
    return render(request, '403.html', status=403)


def custom_500_view(request):
    return render(request, '500.html', status=500)


# === Keresés kombinált (AJAX támogatással) ===
def search_combined(request):
    query = request.GET.get('q', '').strip()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX kérés ellenőrzése
        results = {
            "books": [],
            "employees": []
        }
        if query:
            # Könyvek lekérdezése
            books = Book.objects.filter(title__icontains=query).values('id', 'title', 'author', 'cover_image')
            results['books'] = [
                {
                    'id': book['id'],
                    'title': book['title'],
                    'author': book['author'],
                    'cover_image': f"/media/{book['cover_image']}" if book['cover_image'] else None
                }
                for book in books
            ]
            
            # Munkatársak lekérdezése
            employees = Employee.objects.filter(name__icontains=query)
            results['employees'] = [
                {
                    'name': employee.name,
                    'position': employee.position,
                    'image': employee.image.url if employee.image else None
                }
                for employee in employees
            ]

        return JsonResponse(results)  # JSON válasz
    else:
        return render(request, 'main_kiado/search_results.html', {'query': query})


# === Könyv részletek nézet ===
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'main_kiado/book_detail.html', {'book': book})

def csrf_failure(request, reason=""):
    """
    Egyéni CSRF hibaoldal megjelenítése.
    """
    return render(request, 'main_kiado/csrf_failure.html', {
        'reason': reason,
        'message': _("Érvénytelen CSRF token. Frissítsd az oldalt, majd próbáld újra!")
    }, status=403)