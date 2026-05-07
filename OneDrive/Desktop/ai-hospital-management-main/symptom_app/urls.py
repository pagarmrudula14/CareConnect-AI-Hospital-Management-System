from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("symptoms/", views.symptom_checker, name="symptom_checker"),
    path("result/", views.result, name="result"),
    path("hospitals/", views.hospitals, name="hospitals"),
    path("doctors/", views.doctors, name="doctors"),
    path("appointment/", views.appointment, name="appointment"),
    path("appointment/success/", views.appointment_success, name="appointment_success"),
]
