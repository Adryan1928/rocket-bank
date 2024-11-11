from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signin", views.signin, name="signin"),
    path("signup", views.signup, name="signup"),
    path("real-state-financing/", views.real_state_financing, name="real_state_financing"),
]
