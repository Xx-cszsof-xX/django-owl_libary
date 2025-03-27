from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Review, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'review', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _("Add meg a neved...")}),
            'email': forms.EmailInput(attrs={'placeholder': _("Add meg az email címed...")}),
            'review': forms.Textarea(attrs={'placeholder': _("Írd ide a véleményed...")})
        }
        labels = {
            'name': _("Név"),
            'email': _("Email"),
            'review': _("Vélemény"),
            'rating': _("Értékelés"),
        }


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _("First Name"), 'class': 'form-control'}),
        label=_("Keresztnév")
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _("Last Name"), 'class': 'form-control'}),
        label=_("Vezetéknév")
    )
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _("Username"), 'class': 'form-control'}),
        label=_("Felhasználónév")
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': _("Email"), 'class': 'form-control'}),
        label=_("Email")
    )
    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': _("Password"), 'class': 'form-control'}),
        label=_("Jelszó")
    )
    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': _("Confirm Password"), 'class': 'form-control'}),
        label=_("Jelszó megerősítése")
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name': _("Keresztnév"),
            'last_name': _("Vezetéknév"),
            'username': _("Felhasználónév"),
            'email': _("Email"),
            'password1': _("Jelszó"),
            'password2': _("Jelszó megerősítése"),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'birth_date']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'placeholder': _("Válassz profilképet")
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _("Írd be az életrajzodat...")
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }, format='%Y-%m-%d'),
        }
        labels = {
            'profile_picture': _("Profilkép"),
            'bio': _("Életrajz"),
            'birth_date': _("Születési dátum"),
        }
        help_texts = {
            'profile_picture': _("Kép feltöltése: JPEG vagy PNG formátum ajánlott."),
            'bio': _("Az életrajz rövid szöveges leírás legyen."),
            'birth_date': _("A születési dátum formátuma: ÉÉÉÉ-HH-NN (pl. 1990-01-15)."),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['bio'].widget.attrs.update({'placeholder': _("Írd le magadról röviden...")})
        self.fields['birth_date'].widget.attrs.update({
            'type': 'date',
            'class': 'form-control',
            'placeholder': _("Pl. 1990-01-15")
        })

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            if birth_date.year > 9999 or birth_date.year < 1000:
                raise forms.ValidationError(_("Az évnek 4 számjegyűnek kell lennie."))
        return birth_date
