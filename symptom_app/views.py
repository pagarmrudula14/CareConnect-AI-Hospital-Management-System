import difflib
import requests
from datetime import datetime, date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse

from .models import Hospital, Doctor, Appointment, UserProfile


# =========================================================
# HOME
# =========================================================
def home(request):
    return render(request, "symptom_app/home.html")


# =========================================================
# AUTH
# =========================================================
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return redirect("signup")

        user = User.objects.create_user(username=username, password=password)

        login(request, user)

        return redirect("home")

    return render(request, "symptom_app/signup.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")   # or "symptom_checker"
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "symptom_app/login.html")



def user_logout(request):
    logout(request)
    return redirect("home")


# =========================================================
# HOSPITAL SYSTEM
# =========================================================
@login_required
def hospitals(request):
    return render(request, "symptom_app/hospitals.html", {
        "hospitals": Hospital.objects.all()
    })


@login_required
def doctors(request):
    hospital_id = request.GET.get("hospital")
    doctors = Doctor.objects.filter(hospital_id=hospital_id)
    return render(request, "symptom_app/doctors.html", {"doctors": doctors})


@login_required
def appointment(request):
    doctor_id = request.GET.get("doctor")
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        date_val = request.POST.get("date")
        time_val = request.POST.get("time")

        Appointment.objects.create(
            user=request.user,
            doctor=doctor,
            date=date_val,
            time=time_val
        )

        # ✅ SAFE SMS (never break app)
        try:
            from .views import send_sms   # or wherever you kept it

            message = f"Hi {request.user.username}, your appointment with Dr {doctor.name} is confirmed on {date_val} at {time_val}"

            send_sms(
                phone=request.user.userprofile.phone,
                message=message
            )
        except Exception as e:
            print("SMS Error:", e)

        return redirect("appointment_success")

    return render(request, "symptom_app/appointment.html", {"doctor": doctor})

@login_required
def appointment_success(request):
    return render(request, "symptom_app/appointment_success.html")


@login_required
def appointment_list(request):
    today = date.today()
    upcoming = Appointment.objects.filter(user=request.user, date__gte=today)
    past = Appointment.objects.filter(user=request.user, date__lt=today)

    return render(request, "symptom_app/appointment_list.html", {
        "upcoming_appointments": upcoming,
        "past_appointments": past
    })


# =========================================================
# SYMPTOM CHECKER (KEEP YOUR ORIGINAL LOGIC)
# =========================================================

KNOWN_SYMPTOMS = [
    "fever", "cough", "cold", "headache", "vomiting",
    "diarrhea", "stomach pain", "body pain", "fatigue",
    "sore throat", "dizziness", "nausea", "chest pain",
    "shortness of breath", "rash", "sneezing", "acidity",
    "back pain", "joint pain", "loss of appetite",
    "insomnia", "swelling", "weakness", "runny nose",
    "ear pain"
]


def correct_symptoms(text):
    words = text.lower().split()
    corrected = []

    for w in words:
        match = difflib.get_close_matches(w, KNOWN_SYMPTOMS, n=1, cutoff=0.6)
        corrected.append(match[0] if match else w)

    return " ".join(corrected)


def symptom_ai_engine(s):

    # =====================================================
    # FEVER
    # =====================================================
    if "fever" in s:
        return """
Most likely condition:
Viral Fever / Dengue / Malaria (early stage)

What to eat:
- Khichdi (rice + dal)
- Banana
- Apple
- Coconut water
- Vegetable soup

Foods to avoid:
- Spicy food
- Fried food
- Cold drinks
- Junk food

Home remedies:
1. Cold sponge bath
2. Tulsi (basil) tea
3. Ginger + honey water
4. ORS hydration
5. Proper rest (7–8 hrs)

What to do:
- Drink 3–4L water daily
- Monitor temperature
- Take complete rest

What NOT to do:
- Avoid heat exposure
- Avoid oily food
- Do not skip meals

Doctor needed:
- Fever > 3 days
- Temperature > 102°F
- Severe weakness or rashes

"""

    # =====================================================
    # COUGH
    # =====================================================
    elif "cough" in s or "throat pain" in s:
        return """
Most likely condition:
Cold / Bronchitis / Viral infection

What to eat:
- Warm soup
- Honey
- Ginger tea
- Turmeric milk
- Soft food

Foods to avoid:
- Cold drinks
- Ice cream
- Fried snacks
- Dust exposure

Home remedies:
1. Steam inhalation
2. Salt water gargle
3. Honey + warm water
4. Ginger tea
5. Turmeric milk

What to do:
- Keep throat warm
- Drink fluids
- Rest voice

What NOT to do:
- Avoid smoking
- Avoid cold drinks
- Avoid shouting

Doctor needed:
- Cough > 7 days
- Blood in cough
- Breathing difficulty

"""

    # =====================================================
    # HEADACHE
    # =====================================================
    elif "headache" in s or "stress " in s:
        return """
Most likely condition:
Migraine / Stress / Dehydration

What to eat:
- Bananas
- Almonds
- Walnuts
- Watermelon
- Light food

Foods to avoid:
- Coffee excess
- Alcohol
- Chocolate
- Junk food

Home remedies:
1. Cold compress
2. Rest in dark room
3. Peppermint oil massage
4. Hydration
5. Deep breathing

What to do:
- Reduce screen time
- Sleep properly
- Stay hydrated

What NOT to do:
- Avoid stress
- Avoid skipping meals
- Avoid screen overuse

Doctor needed:
- Frequent severe headaches
- Vision issues

"""

    # =====================================================
    # STOMACH PAIN
    # =====================================================
    elif "stomach" in s or "acidity" in s or "gas " in s:
        return """
Most likely condition:
Gas / Acidity / Gastritis

What to eat:
- Khichdi
- Curd
- Banana
- Rice
- Boiled vegetables

Foods to avoid:
- Spicy food
- Junk food
- Fried food
- Alcohol

Home remedies:
1. Ajwain water
2. Ginger tea
3. Fennel water
4. Warm water
5. Light meals

What to do:
- Eat small meals
- Stay hydrated
- Rest

What NOT to do:
- Do not overeat
- Avoid spicy food
- Avoid alcohol

Doctor needed:
- Severe or persistent pain

"""

    # =====================================================
    # VOMITING
    # =====================================================
    elif "vomitting" in s:
        return """
Most likely condition:
Food poisoning / Infection

What to eat:
- ORS
- Banana
- Rice water
- Toast
- Applesauce

Foods to avoid:
- Spicy food
- Fried food
- Dairy initially
- Junk food

Home remedies:
1. ORS solution
2. Ginger juice
3. Mint water
4. Small sips of water
5. Rest

What to do:
- Hydrate slowly
- Eat light food
- Rest

What NOT to do:
- Avoid solid food initially
- Avoid oily food

Doctor needed:
- Continuous vomiting
- Signs of dehydration

"""

    # =====================================================
    # DIARRHEA
    # =====================================================
    elif "diarrhea" in s:
        return """
Most likely condition:
Infection / Food poisoning

What to eat:
- Rice
- Curd
- Banana
- Khichdi
- Toast

Foods to avoid:
- Spicy food
- Dairy initially
- Junk food

Home remedies:
1. ORS
2. Curd (probiotic)
3. Boiled water
4. Ginger water
5. Rest

What to do:
- Hydration
- Light diet
- Rest

What NOT to do:
- Avoid oily food
- Avoid outside food

Doctor needed:
- Blood in stool
- Severe dehydration

"""

    # =====================================================
    # FATIGUE / WEAKNESS
    # =====================================================
    elif "fatigue" in s or "weakness" in s:
        return """
Most likely condition:
Vitamin deficiency / Weakness / Stress

What to eat:
- Fruits (banana, apple)
- Eggs
- Nuts
- Milk
- Green vegetables

Foods to avoid:
- Junk food
- Excess sugar
- Alcohol

Home remedies:
1. Proper sleep
2. Protein diet
3. Hydration
4. Light exercise
5. Iron-rich food

What to do:
- Maintain sleep cycle
- Eat balanced diet

What NOT to do:
- Avoid skipping meals
- Avoid overwork

Doctor needed:
- Long-term weakness

"""

    # =====================================================
    # DEFAULT CASE
    # =====================================================
    else:
        return """
Most likely condition:
General viral infection

What to eat:
- Light home food
- Fruits
- Soup

Foods to avoid:
- Junk food
- Spicy food

Home remedies:
1. Rest
2. Hydration
3. Steam inhalation
4. ORS
5. Light diet

Doctor needed:
- If symptoms persist >3 days

"""

def symptom_ai_engine(s):

    # =====================================================
    # FEVER
    # =====================================================
    if "fever" in s or " temperature " in s:
        return """
Most likely condition:
Viral Fever / Dengue / Malaria

What to eat:
- Banana, Apple
- Khichdi (rice + dal)
- Coconut water
- Vegetable soup

Foods to avoid:
- Spicy food
- Junk food

Home remedies:
1. Cold sponge bath
2. Tulsi tea
3. ORS hydration
4. Ginger + honey water
5. Rest

What NOT to do:
- Do not overexert
- Avoid oily food

Doctor needed:
- Fever > 3 days or >102°F
"""

    # =====================================================
    # JOINT PAIN
    # =====================================================
    elif "joint pain" in s:
        return """
Most likely condition:
Arthritis / Vitamin deficiency

What to eat:
- Milk, Eggs
- Green vegetables
- Nuts

Foods to avoid:
- Junk food
- Excess sugar

Home remedies:
1. Hot compress
2. Turmeric milk
3. Light exercise
4. Mustard oil massage
5. Rest

Doctor needed:
- Pain > 2 weeks
"""

    # =====================================================
    # TOOTH PAIN
    # =====================================================
    elif "tooth pain " in s:
        return """
Most likely condition:
Cavity / Infection

What to eat:
- Soft food
- Soup

Foods to avoid:
- Sugar
- Cold drinks

Home remedies:
1. Clove oil
2. Salt water rinse
3. Cold compress
4. Turmeric paste
5. Rest

Doctor needed:
- Dentist required
"""

    # =====================================================
    # EYE INFECTION / RED EYES / ITCHING
    # =====================================================
    elif "eye" in s or "red eyes" in s or "itching" in s or "cataract" in s:
        return """
Most likely condition:
Eye infection / Allergy

What to eat:
- Carrots
- Vitamin A foods

Foods to avoid:
- Screen strain
- Dust

Home remedies:
1. Cold compress
2. Clean water wash
3. Rose water drops
4. Rest eyes
5. Hygiene

Doctor needed:
- Pain or vision issues
"""

    # =====================================================
    # FRACTURE / CUT / INJURY / BURNS
    # =====================================================
    elif "fracture" in s or "cut" in s or "burn" in s:
        return """
Most likely condition:
Injury / Fracture / Burn

What to do:
- Immobilize area
- Cold water wash (burns)
- Clean dressing

What NOT to do:
- Do not move injured part

Doctor needed:
- Emergency hospital visit
"""

    # =====================================================
    # NOSE BLEED
    # =====================================================
    elif "nose" in s:
        return """
Most likely condition:
Dry nose / BP / Injury

What to do:
- Sit forward
- Pinch nose 10 min

What NOT to do:
- Do not lie back

Doctor needed:
- Frequent bleeding
"""

    # =====================================================
    # HAIR LOSS / DANDRUFF / GREY HAIR
    # =====================================================
    elif "hair" in s or "dandruff" in s or "grey" in s:
        return """
Most likely condition:
Nutritional deficiency / Stress / Dandruff

What to eat:
- Protein foods
- Nuts
- Eggs

Foods to avoid:
- Junk food

Home remedies:
1. Coconut oil massage
2. Onion juice
3. Aloe vera gel
4. Anti-dandruff shampoo
5. Hydration

Doctor needed:
- Severe hair fall
"""

    # =====================================================
    # CHEST PAIN / ACIDITY
    # =====================================================
    elif "chest pain" in s or "Acidity " in s:
        return """
Most likely condition:
Acidity / Muscle strain / Heart issue

What to eat:
- Light food
- Banana
- Oats

Foods to avoid:
- Spicy food
- Oily food

Home remedies:
1. Deep breathing
2. Rest
3. Warm water

Doctor needed:
- Emergency if severe pain
"""

    # =====================================================
    # KIDNEY STONE
    # =====================================================
    elif "kidney" in s:
        return """
Most likely condition:
Kidney stone

What to eat:
- Watermelon
- Lemon water

Foods to avoid:
- Salt excess

Home remedies:
1. Hydration
2. Coconut water
3. Pain rest

Doctor needed:
- Severe pain emergency
"""

    # =====================================================
    # DIABETES / SUGAR
    # =====================================================
    elif "diabetes" in s or "sugar" in s:
        return """
Most likely condition:
Diabetes

What to eat:
- Green vegetables
- High fiber foods

Foods to avoid:
- Sugar
- White rice

Doctor needed:
- Regular monitoring required
"""

    # =====================================================
    # BP LOW / HIGH
    # =====================================================
    elif "bp" in s:
        return """
Most likely condition:
Blood pressure imbalance

What to do:
- Rest
- Hydration

Doctor needed:
- Regular BP check
"""

    # =====================================================
    # DEPRESSION / STRESS / ANXIETY
    # =====================================================
    elif "depression" in s or "stress" in s or "Anxiety " in s:
        return """
Most likely condition:
Stress / Depression

What to do:
- Talk to someone
- Exercise
- Meditation

Doctor needed:
- Mental health support
"""

    # =====================================================
    # THYROID
    # =====================================================
    elif "thyroid" in s:
        return """
Most likely condition:
Thyroid imbalance

Doctor needed:
- Blood test required
"""

    # =====================================================
    # URINE INFECTION
    # =====================================================
    elif "urine" in s:
        return """
Most likely condition:
UTI infection

What to eat:
- Water
- Cranberry juice

Doctor needed:
- Antibiotics required
"""

    # =====================================================
    # SKIN INFECTION / RASH / ITCHING / PIMPLES / PIGMENTATIONS
    # =====================================================
    elif "skin" in s or "rash" in s or "itch" in s or "pimple" in s or "Pigemnetations" in s:
        return """
Most likely condition:
Skin infection / Allergy

What to do:
- Clean skin
- Aloe vera

Doctor needed:
- If spreading
"""

    # =====================================================
    # MEMORY LOSS / SLEEP PROBLEMS / DARKCIRCLES 
    # =====================================================
    elif "memory" in s or "sleep" in s or "darkcircles" in s:
        return """
Most likely condition:
Stress / Vitamin deficiency

What to do:
- Sleep properly
- Meditation

Doctor needed:
- Persistent issues
"""

    # =====================================================
    # DEFAULT
    # =====================================================
    else:
        return """
Most likely condition:
General health issue

What to do:
- Rest
- Hydration

Doctor needed:
- If symptoms persist >3 days
"""




# =========================================================
# MAIN SYMPTOM CHECKER VIEW (UNCHANGED STRUCTURE)
# =========================================================
@login_required
def symptom_checker(request):
    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "").strip()

        if not symptoms:
            return JsonResponse({"result": "Please enter symptoms"})

        corrected = correct_symptoms(symptoms)
        result = symptom_ai_engine(corrected)

        return JsonResponse({
            "result": result,
            "corrected": corrected,
            "show button": True
        })

    return render(request, "symptom_app/symptom_checker.html")




import requests

def send_sms(phone, message):
    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "route": "q",
        "message": message,
        "language": "english",
        "flash": 0,
        "numbers": phone,
    }

    headers = {
        "authorization": "zUBvR3CX25MifHAmjWEF1rNTQDJhgZ7uatKe6skLldnwYq8c4xI7qQPRC0BWbKAlnejZGwHN9MzhmTav",
 "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()