import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class User(AbstractUser):
    is_viewer = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=True)
    is_supervisor = models.BooleanField(default=False)


class Profile(models.Model):
    GENDER_LIST = [
        ("F", "F"),
        ("M", "M"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to="profile_photos",
        default="default-avatarpng.png",
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_LIST, default=GENDER_LIST[0][0]
    )
    phone = models.TextField(null=True, default="+1")
    phone1 = models.TextField(blank=True)
    bio = models.TextField(blank=True)

    # def get_absolute_url(self):
    #     return reverse("profile", kwargs={"slug": self.slug})

    def get_profile_initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]} {self.last_name[0]}"
        return self.user.email[0]

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.user.email
