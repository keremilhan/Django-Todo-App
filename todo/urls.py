from django.urls import path

from todo.views import *

urlpatterns = [
    path('', home, name="home"),
    path('add/', todo_create, name="add"),
    path('update/<int:id>', todo_update, name="update"),
    path('delete/<int:id>', todo_delete, name="delete"),
    path('todo/<int:id>', todo_details, name="details"),
]
