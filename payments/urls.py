from django.urls import path, re_path
from . import views

app_name = 'payments'

urlpatterns = [
    path("", views.show_payments, name="show_payments"),
    path("add-favorite/", views.add_favorite, name="add_favorite"),
    path("delete-favorite/<int:id>/", views.delete_favorite, name="delete_favorite"),
    re_path(r'^pix(?:/(?P<step>\w+))?/$', views.pix, name='pix'),
    path("depositos/", views.depositos, name="depositos"),
    path("extrato/", views.extrato, name="extrato"),
    path('register_pix/', views.register_pix, name='register_pix'),
]
