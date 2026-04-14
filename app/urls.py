from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('folder/<str:folder>/', views.inbox, name='inbox'),
    path('compose/', views.compose, name='compose'),
    path('email/<int:pk>/', views.email_detail, name='email_detail'),
    path('email/<int:pk>/toggle-star/', views.toggle_star, name='toggle_star'),
    path('email/<int:pk>/delete/', views.delete_email, name='delete_email'),
    path('empty-trash/', views.empty_trash, name='empty_trash'),
]