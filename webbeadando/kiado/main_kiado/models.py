from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from modeltranslation.translator import register, TranslationOptions


class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    position = models.CharField(max_length=100, verbose_name=_("Position"))
    about = models.TextField(default='', verbose_name=_("About"))
    image = models.ImageField(upload_to='employees/', null=True, blank=True, verbose_name=_("Image"))

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    author = models.CharField(max_length=100, verbose_name=_("Author"))
    published_date = models.DateField(verbose_name=_("Published Date"))
    cover_image = models.ImageField(upload_to="books/", blank=True, null=True, verbose_name=_("Cover Image"))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Price"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title


class Review(models.Model):
    email = models.EmailField(verbose_name=_("Email"))
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    review = models.TextField(verbose_name=_("Review"))
    rating = models.IntegerField(
        choices=[(i, _(f"{i} star")) for i in range(1, 6)],
        verbose_name=_("Rating")
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return f"{self.name} - {self.date}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def total_price(self):
        return sum(item.book.price * item.quantity for item in self.items.all())

    def __str__(self):
        return _("%(username)s's Cart") % {'username': self.user.username}


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name=_("Cart"))
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("Book"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")

    def total_item_price(self):
        return self.book.price * self.quantity


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("Book"))
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Purchased At"))

    class Meta:
        verbose_name = _("Purchase")
        verbose_name_plural = _("Purchases")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    bio = models.TextField(blank=True, null=True, verbose_name=_("Bio"))
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name=_("Profile Picture"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Birth Date"))

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return _("%(username)s's Profile") % {'username': self.user.username}
