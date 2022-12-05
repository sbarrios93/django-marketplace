from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"


class UsersPageView(TemplateView):
    user_model = get_user_model()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["users"] = self.user_model.objects.all()
        return context

    template_name = "users.html"


class ProfilePageView(LoginRequiredMixin, DetailView):
    model = get_user_model()

    slug_field: str = "username"
    slug_url_kwarg: str = "username"

    template_name = "profile.html"
