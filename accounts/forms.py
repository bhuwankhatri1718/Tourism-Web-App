from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TouristRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=200, required=True)
    nationality = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password1', 'password2',
            'phone', 'address', 'nationality',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            # accounts.signals already created a blank TouristProfile
            # for this user (OneToOne) - fill it in, don't create a new one.
            profile = user.tourist_profile
            profile.phone = self.cleaned_data['phone']
            profile.address = self.cleaned_data['address']
            profile.nationality = self.cleaned_data['nationality']
            profile.save()

        return user