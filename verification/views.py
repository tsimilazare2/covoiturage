from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import DriverProfileForm, VehicleForm
from .models import DriverProfile, VerificationStatus
from vehicles.models import Vehicle


@login_required
def driver_onboarding(request):
    """Collecte les informations nécessaires à la validation d'un chauffeur."""
    if not request.user.is_driver():
        messages.error(request, 'Cet espace est réservé aux chauffeurs.')
        return redirect('trips:dashboard')

    profile, _ = DriverProfile.objects.get_or_create(user=request.user)
    vehicle = Vehicle.objects.filter(owner=request.user).order_by('id').first()
    profile_form = DriverProfileForm(request.POST or None, request.FILES or None, instance=profile)
    vehicle_form = VehicleForm(request.POST or None, request.FILES or None, instance=vehicle)
    if request.method == 'POST' and profile_form.is_valid() and vehicle_form.is_valid():
        profile = profile_form.save(commit=False)
        profile.user = request.user
        profile.status = VerificationStatus.EN_ATTENTE
        profile.submitted_at = timezone.now()
        profile.save()
        vehicle = vehicle_form.save(commit=False)
        vehicle.owner = request.user
        vehicle.is_verified = False
        vehicle.save()
        messages.success(request, 'Vos informations ont été envoyées pour vérification.')
        return redirect('trips:dashboard')
    return render(request, 'verification/driver_onboarding.html', {'profile_form': profile_form, 'vehicle_form': vehicle_form, 'profile': profile})
