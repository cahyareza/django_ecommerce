from django.contrib.auth import get_user_model
from django import forms

# check for unique email & username
non_allowed_usenames = ["abc"]
User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password"
            }
        )
    )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )

    #def clean(self):
     #   username = self.cleaned_data.get("username")
    #  password = self.cleaned_data.get("password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # thisIsMyUsername == thisismyusername
        qs = User.objects.filter(username_iexact=username)
        if username in non_allowed_usenames:
            raise forms.ValidationError("This is an invalid username, please pick another.")
        if not qs.exist():
            raise forms.ValidationError("This is an invalid username, please pick another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # thisIsMyUsername == thisismyusername
        qs = User.objects.filter(email_iexact=email)
        if not qs.exist():
            raise forms.ValidationError("This email is already in use")
        return email