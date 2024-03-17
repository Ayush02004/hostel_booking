from django.urls import path
from . import views

urlpatterns = [
    # ... other URL patterns ...
    path('', views.create_user, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.login_view, name='logout')
]
