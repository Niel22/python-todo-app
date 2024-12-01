from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    path('add/', views.add_todo, name="add_todo"),
    path('delete/<int:id>/', views.delete_todo, name="delete_todo"),
    path('update/<int:id>/', views.update_todo, name="update_todo")
]
