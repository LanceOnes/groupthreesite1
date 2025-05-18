from django.urls import path
from . import views

urlpatterns = [
    path('gender/list', views.gender_list),
    path('gender/add', views.add_gender),
    path('gender/edit/<int:genderId>', views.edit_gender),
    path('gender/delete/<int:genderId>', views.delete_gender),
    
    path('user/add', views.add_user, name='add_user'),
    path('user/edit/<int:userId>', views.edit_user),
    path('user/list/', views.user_list),    
    path('user/delete/<int:userId>', views.delete_user),
    
    path('user/change_password/<int:userId>', views.change_password),
    path('user/password/<int:userId>/', views.password, name='password'),
    
   path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),  # Default login route
    path('', views.login_view, name='login'),  # Root URL redirects to login
    path('signup/', views.signup_view, name='signup'),  # Signup route

]