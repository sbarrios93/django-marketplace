from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model


class CustomSignupForm(SignupForm):
    private_profile = forms.BooleanField(
        required=False,
        label="Private Profile",
        initial=False,
    )

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        # Add your own processing here.
        user.private_profile = self.cleaned_data.get("private_profile")
        user.save()

        # You must return the original result.
        return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "private_profile",
        )
