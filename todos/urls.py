from django.urls import path
from todos import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login-page', views.login_page, name='login-page'),
    path('logout-page', views.logout_page, name='logout-page'),
    path('register', views.register, name='register'),
    path('todo', views.todo, name='todo'),
    path('delete_task/<int:pk>', views.delete_task, name='delete-task'),
    path('edit_task/<int:pk>', views.edit_task, name='edit-task'),
]