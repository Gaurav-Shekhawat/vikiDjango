from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/newPage",views.newPage,  name = "newPage"),
    path("wiki/<str:pagetitle>", views.entry, name = "entry"),
]
