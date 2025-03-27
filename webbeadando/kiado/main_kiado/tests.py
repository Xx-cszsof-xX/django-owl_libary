from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Review, Employee, Cart, CartItem, Profile, Purchase

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test_home_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_renders_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main_kiado/home.html')

class AboutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('about')

    def test_about_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_about_view_renders_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main_kiado/about.html')

class EmployeesViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('employees')
        Employee.objects.create(name="John Doe", position="Developer")

    def test_employees_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_employees_view_renders_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main_kiado/employees.html')

    def test_employees_view_context(self):
        response = self.client.get(self.url)
        self.assertIn('employees', response.context)
        self.assertEqual(len(response.context['employees']), 1)

class BooksViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('books')
        Book.objects.create(title="Test Book", author="Test Author")

    def test_books_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_books_view_renders_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main_kiado/books.html')

    def test_books_view_context(self):
        response = self.client.get(self.url)
        self.assertIn('books', response.context)
        self.assertEqual(len(response.context['books']), 1)

class AddToCartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.book = Book.objects.create(title="Test Book", author="Test Author")
        self.url = reverse('add_to_cart', args=[self.book.id])

    def test_add_to_cart_redirects_if_not_logged_in(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_add_to_cart_creates_cart_item(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, {'quantity': 1})
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, book=self.book)
        self.assertEqual(cart_item.quantity, 1)

class ReviewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('reviews')
        self.review_data = {
            'title': 'Great Book!',
            'content': 'Loved it!',
            'rating': 5
        }

    def test_reviews_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_reviews_view_renders_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main_kiado/reviews.html')

    def test_reviews_view_post_creates_review(self):
        response = self.client.post(self.url, data=self.review_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.title, self.review_data['title'])

class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('search_combined')
        self.book = Book.objects.create(title="Django Unleashed", author="Andrew Pinkham")

    def test_search_combined_returns_results(self):
        response = self.client.get(self.url, {'q': 'Django'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('books', response.json())
        self.assertEqual(len(response.json()['books']), 1)
        self.assertEqual(response.json()['books'][0]['title'], "Django Unleashed")

    def test_search_combined_no_results(self):
        response = self.client.get(self.url, {'q': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['books']), 0)

class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.url = reverse('profile')

    def test_profile_view_redirects_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_profile_view_displays_correctly(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_kiado/profile.html')

