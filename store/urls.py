from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path('', views.index, name='index'),
    path('dept/<str:pk>', views.dept, name='department'),
    path('newstock', views.newstock, name='newstock'),
    path('history/<str:pk>', views.history, name='dept_history'),
    path('history/<str:pk>/<str:item>', views.history, name='item_history'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
