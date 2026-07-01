from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove default help texts untuk tampilan minimalis
        self.fields["username"].help_text = None
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None

        # Styling labels dan placeholders
        self.fields["username"].label = "Full Name"
        self.fields["username"].widget.attrs.update({
            "placeholder": "ALEXANDER VANCE",
            "class": "w-full bg-transparent border-0 border-b border-outline-variant py-3 px-0 font-body-md text-body-md focus-ring transition-all placeholder:text-outline-variant"
        })

        self.fields["email"].widget.attrs.update({
            "placeholder": "vance@academia.edu",
            "class": "w-full bg-transparent border-0 border-b border-outline-variant py-3 px-0 font-body-md text-body-md focus-ring transition-all placeholder:text-outline-variant"
        })

        self.fields["password1"].label = "Secure Password"
        self.fields["password1"].widget.attrs.update({
            "placeholder": "••••••••••••",
            "class": "w-full bg-transparent border-0 border-b border-outline-variant py-3 px-0 font-body-md text-body-md focus-ring transition-all placeholder:text-outline-variant"
        })

        self.fields["password2"].label = "Confirm Password"
        self.fields["password2"].widget.attrs.update({
            "placeholder": "••••••••••••",
            "class": "w-full bg-transparent border-0 border-b border-outline-variant py-3 px-0 font-body-md text-body-md focus-ring transition-all placeholder:text-outline-variant"
        })

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email ini sudah terdaftar.")
        return email


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["username"].label = "Email Address"
        self.fields["username"].widget.attrs.update({
            "placeholder": "name@institute.edu",
            "class": "w-full bg-transparent border-0 border-b border-outline-variant py-3 px-0 font-body-md text-body-md focus:ring-0 focus:border-primary transition-all placeholder:text-outline-variant"
        })

        self.fields["password"].widget.attrs.update({
            "placeholder": "••••••••",
            "class": "w-full bg-transparent border-0 border-b border-outline-variant py-3 px-0 font-body-md text-body-md focus:ring-0 focus:border-primary transition-all placeholder:text-outline-variant"
        })

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Izinkan login dengan email
        if username and "@" in username:
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                pass
        return username