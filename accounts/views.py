from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import CustomLoginForm, CustomRegisterForm


class RegisterView(CreateView):
    model = User
    form_class = CustomRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("courses:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Auto login setelah register
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "accounts/login.html"

    def get_success_url(self):
        # Jika ada ?next= di URL, pakai itu. Else ke home.
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("courses:home")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("courses:home")