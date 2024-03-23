from django.urls import include, path
from django_registration.backends.activation import views as register_views

from .forms import RegistrationForm
from . import views

urlpatterns = [
    path(
        "register/",
        register_views.RegistrationView.as_view(form_class=RegistrationForm),
        name="django_registration_register",
    ),
    path("", include("django_registration.backends.activation.urls")),
    path("", include("django.contrib.auth.urls")),
    path("preferences/", views.PreferencesUpdateView.as_view(), name="preferences"),
    path("preferences/delete-user/", views.UserDeleteView.as_view(), name="user_delete"),
    path("preferences/worker/", views.WorkerAdministrationView.as_view(), name="preferences_worker"),
    path("preferences/worker/<str:action>/", views.WorkerAdministrationView.as_view(), name="preferences_worker"),
    path("", views.WishListView.as_view(), name="wish_list"),
    path("create/", views.WishCreateView.as_view(), name="wish_create"),
    path("detail/<int:pk>", views.WishDetailView.as_view(), name="wish_detail"),
    path("delete/<int:pk>", views.WishDeleteView.as_view(), name="wish_delete"),
]
