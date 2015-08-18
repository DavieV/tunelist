from django import forms
from django.contrib.auth.models import User

class PlaylistForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)

class SongForm(forms.Form):
    song_url = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'URL'})
    )
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'})
    )

    artist = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Artist'})
    )

class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm Password", 
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match each other")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already in use")

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )

