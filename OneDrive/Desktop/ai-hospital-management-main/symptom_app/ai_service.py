def predict_disease(symptoms):
    symptoms = symptoms.lower()

    # 🦠 Infections
    if "fever" in symptoms and "cough" in symptoms:
        return "Flu"

    if "fever" in symptoms and "cold" in symptoms:
        return "Viral Fever"

    if "sore throat" in symptoms:
        return "Throat Infection"

    if "fever" in symptoms and "rash" in symptoms:
        return "Measles"

    if "fever" in symptoms and "joint pain" in symptoms:
        return "Dengue"

    if "loss of taste" in symptoms or "loss of smell" in symptoms:
        return "COVID-19"

    # 🧠 Neurological
    if "headache" in symptoms and "vomiting" in symptoms:
        return "Migraine"

    if "dizziness" in symptoms and "blurred vision" in symptoms:
        return "Vertigo"

    if "seizure" in symptoms:
        return "Epilepsy"

    # ❤️ Cardiac
    if "chest pain" in symptoms and "shortness of breath" in symptoms:
        return "Heart Disease"

    if "chest pain" in symptoms:
        return "Cardiac Issue"

    # 🫁 Respiratory
    if "breathing difficulty" in symptoms:
        return "Asthma"

    if "wheezing" in symptoms:
        return "Bronchitis"

    if "persistent cough" in symptoms:
        return "Respiratory Infection"

    # 🦴 Bones & Injury
    if "swelling" in symptoms and "pain" in symptoms:
        return "Fracture"

    if "joint pain" in symptoms:
        return "Arthritis"

    if "back pain" in symptoms:
        return "Spinal Problem"

    # 🍽️ Digestive
    if "stomach pain" in symptoms and "vomiting" in symptoms:
        return "Food Poisoning"

    if "diarrhea" in symptoms:
        return "Gastroenteritis"

    if "acidity" in symptoms or "heartburn" in symptoms:
        return "Acid Reflux"

    if "constipation" in symptoms:
        return "Digestive Disorder"

    # 🩺 General
    if "fatigue" in symptoms and "weakness" in symptoms:
        return "Anemia"

    if "weight loss" in symptoms:
        return "Metabolic Disorder"

    if "frequent urination" in symptoms and "thirst" in symptoms:
        return "Diabetes"

    # 🧴 Skin
    if "itching" in symptoms and "rash" in symptoms:
        return "Skin Allergy"

    if "dry skin" in symptoms:
        return "Dermatitis"

    # 😴 Mental Health
    if "stress" in symptoms and "anxiety" in symptoms:
        return "Anxiety Disorder"

    if "sadness" in symptoms and "sleep problem" in symptoms:
        return "Depression"

    # 🩹 Default
    return "General Illness"
