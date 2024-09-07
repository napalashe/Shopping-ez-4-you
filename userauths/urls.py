from django.urls import path
from userauths import views

app_name = 'userauths'

urlpatterns = [
    path('sign-up/', views.register_view, name ='sign-up'),
    path('sign-in/', views.login_view, name ='sign-in'),
    path('sign-out/', views.logout_view, name ='sign-out'),
    path('account/', views.account_view, name = 'account'),
    path('edit-profile/', views.edit_profile, name = 'edit-profile'),
    path('logout/', views.logout_view, name = 'logout'),


]