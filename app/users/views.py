from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, UpdateView

from .models import Profile, User


class ProfileListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Profile

    def test_func(self):
        return self.request.user.is_supervisor

    def handle_no_permission(self):
        messages.info(self.request, "Something went wrong")
        return redirect("cheque-list")


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ["image", "first_name", "last_name", "gender", "phone", "phone1", "bio"]
    slug_field = "uid"

    def test_func(self):
        return self.request.user.is_supervisor or self.request.user == self.get_object().user

    def handle_no_permission(self):
        messages.info(self.request, "Something went wrong")
        return redirect("cheque-list")


class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Profile
    slug_field = "uid"

    def test_func(self):
        return self.request.user.is_supervisor or self.request.user == self.get_object().user

    def handle_no_permission(self):
        messages.info(self.request, "Something went wrong")
        return redirect("cheque-list")
