from django.urls import path
from gmailverify import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.userlogin),
    path('verifyscreen/<rid>',views.verifygmail),
    path('verifyotp/<rid>',views.verifyotp),
]