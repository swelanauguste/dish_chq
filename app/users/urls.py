from django.urls import path

from .views import ProfileDetailView, ProfileListView, ProfileUpdateView

urlpatterns = [
    path("", ProfileListView.as_view(), name="profile-list"),
    path("detail/<slug:slug>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("update/<slug:slug>/", ProfileUpdateView.as_view(), name="profile-update"),
]
