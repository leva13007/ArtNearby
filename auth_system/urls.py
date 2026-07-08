from django.urls import path
from auth_system import views
from find_it.views import index

urlpatterns = [
    path("", index, name = "index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile")
]