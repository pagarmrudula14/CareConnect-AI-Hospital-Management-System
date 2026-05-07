print("VIEWS FILE LOADED")
from .ai_service import predict_disease



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Hospital, Doctor, Appointment, UserProfile


def home(request):
    return render(request, "symptom_app/home.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "symptom_app/signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(user=user, phone=phone)

        login(request, user)
        return redirect("symptom_checker")

    return render(request, "symptom_app/signup.html")


def user_login(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("symptom_checker")

    return render(request, "symptom_app/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def symptom_checker(request):
    return render(request, "symptom_app/symptom_checker.html")


@login_required
def result(request):
    symptoms = request.POST.get("symptoms", "")
    disease = predict_disease(symptoms)

    return render(request, "symptom_app/result.html", {
        "disease": disease
    })




@login_required
def hospitals(request):
    return render(request, "symptom_app/hospitals.html", {
        "hospitals": Hospital.objects.all()
    })


@login_required
def doctors(request):
    hospital_id = request.GET.get("hospital")
    doctors = Doctor.objects.filter(hospital_id=hospital_id)

    return render(request, "symptom_app/doctors.html", {
        "doctors": doctors
    })


@login_required
def appointment(request):
    doctor_id = request.GET.get("doctor")
    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")

        appointment = Appointment.objects.create(
            user=request.user,
            doctor=doctor,
            date=date,
            time=time
        )

        return render(request, "symptom_app/appointment_summary.html", {
            "appointment": appointment
        })

    return render(request, "symptom_app/appointment.html", {
        "doctor": doctor
    })


@login_required
def appointment_success(request):
    return render(request, "symptom_app/appointment_success.html")
