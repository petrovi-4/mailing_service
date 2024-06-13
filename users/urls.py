from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    RegisterView, UserUpdateView, generate_new_password, UserListView, UserDetailView, UserDeleteView, email_verification
)

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit_user/<int:pk>/', UserUpdateView.as_view(), name='edit_user'),
    path('generate_password/', generate_new_password, name='generate_new_password'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('view_user/<int:pk>/', UserDetailView.as_view(), name='view_user'),
    path('delete_user/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
    path('confirm/<str:token>/', email_verification, name='confirm'),
]
