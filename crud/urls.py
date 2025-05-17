from django.urls import path
from . import views

urlpatterns = [
    path('gender/list', views.gender_list),
    path('gender/add', views.add_gender),
    path('gender/edit/<int:genderId>', views.edit_gender),
    path('gender/delete/<int:genderId>', views.delete_gender),
    
    path('user/add', views.add_user, name='add_user'),
    path('login/', views.login_view, name='login'),
    path('user/edit/<int:userId>', views.edit_user),
    path('user/list/', views.user_list),    
    path('user/delete/<int:userId>', views.delete_user),
]