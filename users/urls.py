from django.urls import path
from .views import register,user_login,user_logout, user_details


urlpatterns = [
    path('register/',register,name='register'),
    path('login/',user_login,name='user_login'),
    path('logout/', user_logout,name="user_logout"),
    path('details/<int:id>', user_details,name="user_details"),
]
