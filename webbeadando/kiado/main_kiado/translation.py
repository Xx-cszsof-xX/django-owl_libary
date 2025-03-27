from modeltranslation.translator import register, TranslationOptions
from .models import Employee, Book, Review,Profile

@register(Employee)
class EmployeeTranslationOptions(TranslationOptions):
    fields = ('name', 'position', 'about',)

@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('name', 'review',)

@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('bio', ) 