from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class LoginForm(forms.Form):
    email_login = forms.EmailField(label="Email Address", widget=forms.TextInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Email Address'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Password'})
    )


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Last Name'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Email Address'}))
    phone = forms.CharField(label="Phone Number", widget=forms.TextInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Phone Number'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Password Confirmation'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = False

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class ShippingForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Address', 'required': True}))
    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'City', 'required': True}))
    state = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'State/Province', 'required': True}))
    zip_code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Zip code', 'pattern': "[0-9]+", 'required': True}))
    country = CountryField(blank_label='(Select country)').formfield(widget=CountrySelectWidget(
        attrs={"class": "form-select", 'required': True}
    ))
