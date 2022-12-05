from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView

from photos.models import Photo


class HomePageView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_model = get_user_model()
        all_public_users = user_model.objects.filter(private_profile=False)

        public_photos = Photo.objects.filter(owner__in=all_public_users)
        context["photos"] = public_photos
        return context

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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        if view_profile != self.request.user:
            if self.request.user.id in view_profile.get_followers():
                context["follow_status"] = "following"
            elif self.request.user.id in view_profile.get_pending_follow_requests():
                context["follow_status"] = "pending"
            else:
                context["follow_status"] = "not-following"

        if view_profile.private_profile and view_profile != self.request.user:
            if self.request.user.id in view_profile.get_followers():
                context["allowed_viewing"] = True
        else:
            context["allowed_viewing"] = True
        return context

    template_name = "profile.html"


def follow_toggle(request, username):
    user_model = get_user_model()
    recipient_user = user_model.objects.get(username=username)
    sender_user = user_model.objects.get(username=request.user.username)
    following = sender_user.get_following()

    if recipient_user.id in following:
        sender_user.remove_following(recipient_user)
    elif sender_user in recipient_user.get_pending_follow_requests():
        sender_user.remove_following(recipient_user)
    else:
        sender_user.send_follow_request(recipient_user)
    return redirect("profile", username=recipient_user.username)
