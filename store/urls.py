from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path('', views.index, name='index'),
    path('dept', views.dept, name='department'),
    path('newstock', views.newstock, name='newstock'),
    path('history', views.history, name='dept_history'),
    path('department', views.department, name='department'),
    path('history/<str:item>', views.history, name='item_history'),
    path('outofstock', views.outOfStock, name='outofstock'),
    path('supliers', views.suppliers, name='supliers'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('delete/<str:id>', views.delete,name='delete'),
    path('removedepartment/<str:id>', views.removeDept, name='removedepartemnt')
]
