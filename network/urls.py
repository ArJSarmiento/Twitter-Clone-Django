
from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.add_post, name="add_post"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("follow_user/<int:follow_id>", views.follow_user, name="follow_user"),
    path("follow_status/<int:status_id>", views.follow_status, name="follow_status"),
    path("is_mypost/<int:post_id>", views.is_mypost, name="is_mypost"),
    path("edit_post/<int:edit_id>", views.edit_post, name="edit_post"),
    path("like_post/<int:like_id>", views.like_post, name ="like_post"),
    path("is_liked/<int:islike_id>", views.is_liked, name ="is_liked")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)