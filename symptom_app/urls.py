from django.urls import path
from . import views



from django.shortcuts import render

def home(request):
    return render(request, "symptom_app/home.html")





urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("symptom-checker/", views.symptom_checker, name="symptom_checker"),
   
    path("hospitals/", views.hospitals, name="hospitals"),
    path("doctors/", views.doctors, name="doctors"),
    path("appointment/", views.appointment, name="appointment"),
    path("appointment/success/", views.appointment_success, name="appointment_success"),
    path('appointments/', views.appointment_list, name='appointment_list'),
    




]