from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("change_password/", views.change_password, name="change_password"),
    path("admin_panel/", views.admin_panel, name="admin_panel"),
    path("admin_panel/unblock/<int:user_id>/", views.unblock_user, name="unblock_user"),
    path('admin_panel/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin_panel/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path("user_panel/", views.user_panel, name="user_panel"),
]
