from django.urls import path
from auth_app import views

urlpatterns = [
    path('Register',views.register, name ='Register'),
    path('Login',views.sign_in, name ='Login'),
    path('Logout',views.sign_out, name ='Logout'),
    path('profile',views.profile, name ='profile'),
    path('editpin/<int:id>',views.editpin, name ='editpin'),
    path('editpro',views.profile_edit, name ='editpro'),
    path('delete/<int:id>',views.del_user, name ='delete')

   
]