from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Employee, Book, Review, Cart, CartItem, Purchase, Profile

# === Employee Admin ===
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'image']
    search_fields = ['name', 'position']
    list_filter = ['position']
    verbose_name = _("Employee")
    verbose_name_plural = _("Employees")

# === Book Admin ===
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date', 'price']
    search_fields = ['title', 'author']
    list_filter = ['published_date', 'price']

# === Review Admin ===
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'rating', 'date']
    search_fields = ['name', 'email']
    list_filter = ['rating', 'date']

# === Cart Item Inline ===
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

# === Cart Admin ===
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

# === Purchase Admin ===
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'purchased_at']
    list_filter = ['user', 'purchased_at']
    search_fields = ['user__username', 'book__title']

# === Profile Admin ===
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'birth_date', 'profile_picture']
    search_fields = ['user__username']
