from django.db import models

# Create your models here.


class Photo(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    caption = models.CharField(max_length=200)
    owner = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)


class Like(models.Model):
    fan = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    photo = models.ForeignKey("Photo", on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    photo = models.ForeignKey("Photo", on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
