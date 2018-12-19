from django.contrib import messages
from django.contrib.auth import views as auth_views, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from users.forms import LoginForm, RegisterUserForm, UpdateUserForm, UpdateProfileForm


class LoginUserView(View):
    def get(self, request):
        form = LoginForm
        return render(request, "users/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = User.objects.filter(email=email.lower())[0]
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                messages.error(request, 'Błędny login lub hasło')
        return render(request, 'users/login.html', {'form': form})


class LogoutUserView(auth_views.LogoutView):
    template_name = 'users/logout.html'


class RegisterUserView(View):
    def get(self, request):
        form = RegisterUserForm
        return render(request, "users/login.html", {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Utworzono konto dla użytkownika o adresie e-mail {email}')
            return redirect('login')
        return render(request, "users/login.html", {'form': form})


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        update_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        return render(request, "users/profile.html", {'u_form': update_form, 'p_form': profile_form})

    def post(self, request):
        update_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if update_form.is_valid() and profile_form.is_valid():
            update_form.save()
            profile_form.save()
            messages.success(request, f'Twoje konto zostało zmodyfikowane')
            return redirect('profile')
        return render(request, "users/profile.html", {'u_form': update_form, 'p_form': profile_form})


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, "users/password_reset.html", locals())

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            auth_views.update_session_auth_hash(request, user)
            messages.success(request, f'Twoje hasło zostało zmienione')
            return redirect('profile')
        else:
            messages.error(request, 'Wprowadzone dane są nieprawidłowe')
        return render(request, "users/password_reset.html", locals())


class DeleteAccountView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy('login')
    template_name = 'users/user_confirm_delete.html'

    def test_func(self):
        user = self.get_object()
        if self.request.user.id == user.id:
            return True
        else:
            return False
