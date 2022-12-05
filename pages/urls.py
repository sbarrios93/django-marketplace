from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

import pages.views

users_urlpatterns = [
    path("", pages.views.UsersPageView.as_view(), name="users"),
    path("<str:username>", pages.views.ProfilePageView.as_view(), name="profile"),
]

urlpatterns = [
    path("", pages.views.HomePageView.as_view(), name="home"),
    path("users/", include(users_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
