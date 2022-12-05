from django.contrib import messages
from django.contrib.auth import get_user, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render

from accounts.forms import EditProfileForm


# Create your views here.
@login_required()
def edit_profile(request):
    if request.method == "POST" and "email" in request.POST:
        form = EditProfileForm(request.POST, instance=get_user(request))
        if form.is_valid():
            form.save()
            context = {
                "saved": True,
                "form": EditProfileForm(instance=get_user(request)),
                "password_form": PasswordChangeForm(get_user(request)),
            }
            return render(request, "account/edit_profile.html", context)
        else:
            messages.error(request, form.errors)
    if request.method == "POST" and "old_password" in request.POST:
        form = PasswordChangeForm(get_user(request), request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            context = {
                "saved": True,
                "form": EditProfileForm(instance=get_user(request)),
                "password_form": PasswordChangeForm(get_user(request)),
            }
            return render(request, "account/edit_profile.html", context)
        else:
            messages.error(request, "Please correct the error below.")
        return redirect("edit_profile")

    else:
        context = {
            "saved": False,
            "form": EditProfileForm(instance=get_user(request)),
            "password_form": PasswordChangeForm(get_user(request)),
        }
        return render(request, "account/edit_profile.html", context)
