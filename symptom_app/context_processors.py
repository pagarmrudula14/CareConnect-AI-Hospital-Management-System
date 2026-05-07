from django.utils import timezone

def navbar_appointments(request):
    if request.user.is_authenticated:
        from .models import Appointment

        today = timezone.localdate()  # ✅ correct for DateField

        upcoming = Appointment.objects.filter(
            user=request.user,
            date__gte=today
        ).order_by('date', 'time')[:3]

        past = Appointment.objects.filter(
            user=request.user,
            date__lt=today
        ).order_by('-date', '-time')[:3]

        return {
            'nav_upcoming_appointments': upcoming,
            'nav_past_appointments': past,
        }

    return {}
