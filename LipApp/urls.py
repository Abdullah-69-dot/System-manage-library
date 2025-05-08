from django.contrib import admin
from django.urls import path , include
from .views import *
urlpatterns = [
    path('',index,name="index"),
    path('books/',books,name="books"),
    path('up/<int:id>',update,name="update"),
    path('del/<int:id>',delete,name="delete")
]
