from django import forms
from .models import Book, CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price']


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('user', 'Обычный пользователь'),
        ('admin', 'Администратор'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Роль")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "role")

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data["role"] == "admin":
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user


class ProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')