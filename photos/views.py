from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView
from django.views.generic.edit import FormMixin

from .forms import CommentForm, NewPhotoForm
from .models import Comment, Like, Photo

# Create your views here.


class PhotoView(LoginRequiredMixin, FormMixin, DetailView):
    model = Photo
    form_class = CommentForm

    def get_success_url(self) -> str:
        return reverse("photo", kwargs={"pk": self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = self.get_object()
        owner = photo.owner
        comments = Comment.objects.filter(photo=photo)
        likes = Like.objects.filter(photo=photo)

        if owner.private_profile and owner != self.request.user:
            if self.request.user.id in owner.get_followers():
                context["allowed_viewing"] = True
        else:
            context["allowed_viewing"] = True
        context["comments"] = comments

        if len(likes) == 0:
            like_string = "No likes yet"
        elif len(likes) == 1:
            like_string = f"{likes[0].fan.username} liked this"
        elif len(likes) <= 3:
            like_string = (
                f"Liked by {', '.join( [like.fan.username for like in likes[:-1]])}"
            )
        else:
            like_string = (
                f"Liked by {likes[0].fan.username}, {likes[1].fan.username},"
                f" {likes[2].fan.username} and {len(likes) - 3} others"
            )
        context["like_string"] = like_string

        if self.request.user.is_authenticated:
            if self.request.user.id in [like.fan.id for like in likes]:
                context["liked"] = True

        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.photo = self.get_object()
        comment.save()
        return super().form_valid(form)

    template_name = "photo.html"


def like_toggle(request, pk):
    user_model = get_user_model()
    fan_user = user_model.objects.get(username=request.user.username)
    photo_object = Photo.objects.get(id=pk)

    if photo_object.id in fan_user.get_liked_photos():
        fan_user.unlike_photo(pk)
    else:
        fan_user.like_photo(pk)

    return redirect("photo", pk=pk)


class NewPhotoView(LoginRequiredMixin, FormView):
    form_class = NewPhotoForm

    def get_success_url(self):
        return reverse("profile", kwargs={"username": self.request.user.username})

    def form_valid(self, form):
        form = form.save(commit=False)
        form.owner = self.request.user
        form.save()
        return super().form_valid(form)

    template_name = "new_photo.html"
