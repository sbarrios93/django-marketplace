from django.forms import ModelForm

from .models import Comment, Photo


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)


class NewPhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ("image", "caption")
