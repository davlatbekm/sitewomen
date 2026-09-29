import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control w-75', 'placeholder': 'Password'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'Username'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control w-75', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="Repeat the password", widget=forms.PasswordInput(
        attrs={'class': 'form-control w-75', 'placeholder': 'Repeat password'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'email': 'E-mail',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control w-75', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'Last Name'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


class ProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'Username'}))
    email = forms.CharField(disabled=True,label='E-mail',
                            widget=forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'E-mail'}))
    this_year = datetime.date.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5)), attrs={'class':'form-control w-75'}), label='Date of Birth',)
    class Meta:
        model = get_user_model()
        fields = ('photo', 'username', 'email', 'date_birth' ,'first_name', 'last_name')
        labels = {'first_name': 'First Name', 'last_name': 'Last Name'}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control w-75', 'placeholder': 'Last Name'}),
            'photo': forms.FileInput(attrs={'class': 'form-control w-75'}),
        }

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control w-75', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control w-75', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control w-75', 'placeholder': 'Repeat password'}))



# forms.py
from django.contrib.auth.forms import (
    PasswordResetForm, SetPasswordForm, PasswordChangeForm
)

class StyledPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control w-75'})


class StyledSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control w-75'})


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control w-75'})