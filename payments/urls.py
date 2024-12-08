from django.urls import path, re_path
from . import views

urlpatterns = [
    path("<int:id>/", views.show_payments, name="show_payments"),
    path("<int:id>/add-favorite/", views.add_favorite, name="add_favorite"),
    path("<int:id>/delete-favorite/", views.delete_favorite, name="delete_favorite"),
    re_path(r'^(?P<id>\d+)/pix(?:/(?P<step>\w+))?/$', views.pix, name='pix'),
    path("<int:id>/depositos/", views.depositos, name="depositos"),
    path("extrato/", views.extrato, name="extrato"),
]
