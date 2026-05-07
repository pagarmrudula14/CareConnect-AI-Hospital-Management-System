from django.contrib import admin
from .models import Hospital, Doctor, Appointment, UserProfile

admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(UserProfile)


