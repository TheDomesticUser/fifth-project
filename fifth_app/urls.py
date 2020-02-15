from django.urls import path
from fifth_app import views

# template urls
app_name = 'fifth_app'

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
]