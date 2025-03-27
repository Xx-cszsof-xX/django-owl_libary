from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from .views import admin_purchase_list
from .views import RegisterView
from .views import profile_view
from django.urls import re_path
from django.views.static import serve
from . import views 
from .views import book_detail, search_combined

urlpatterns = [
    path('admin/purchases/', admin_purchase_list, name='admin_purchase_list'),
]


handler404 = 'main_kiado.views.custom_404_view'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('employees/', views.employees, name='employees'),
    path('contact/', views.contact, name='contact'),
    path('books/', views.books, name='books'),
    path('reviews/', views.reviews, name='reviews'),
    path('cart/', views.view_cart, name='cart'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),    path('checkout/', views.checkout, name='checkout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('purchase/<int:book_id>/', views.purchase_book, name='purchase_book'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='main_kiado/login.html'), name='login'),
    path('admin/purchases/', admin_purchase_list, name='admin_purchase_list'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/', profile_view, name='profile'),
    # path('ajax/search-books/', views.search_books, name='search_books'),
    # path('search/', views.search_books, name='search_books'),
    # path('search_books/', views.search_books, name='search_books'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('ajax/search/', views.search_combined, name='search_combined'),
    path('book/<int:pk>/', book_detail, name='book_detail'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)