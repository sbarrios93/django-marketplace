from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

import photos.views

urlpatterns = [
    path("<int:pk>", photos.views.PhotoView.as_view(), name="photo"),
    path("like/<int:pk>", photos.views.like_toggle, name="like_toggle"),
    path("new/", photos.views.NewPhotoView.as_view(), name="new_photo"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
