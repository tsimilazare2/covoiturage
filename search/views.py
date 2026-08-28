from django.shortcuts import render
from django.db.models import Q

from routes.models import Route
from trips.models import TripOffer, TripStatus


def search_trips(request):
    """Vue de recherche de trajets avec filtres.
    
    Filtres disponibles :
    - départ / point_depart
    - destination
    - date_depart
    - heure_depart (optionnel)
    - prix min/max
    - nombre_places
    - chauffeur_verifie
    """
    trips = TripOffer.objects.filter(statut=TripStatus.PUBLISHED).select_related('driver', 'route', 'vehicle')
    routes = Route.objects.filter(active=True)

    # Récupérer les parameters de recherche du formulaire
    point_depart = request.GET.get('point_depart', '').strip()
    destination = request.GET.get('destination', '').strip()
    date_depart = request.GET.get('date_depart', '').strip()
    heure_depart = request.GET.get('heure_depart', '').strip()
    prix_min = request.GET.get('prix_min', '').strip()
    prix_max = request.GET.get('prix_max', '').strip()
    nombre_places = request.GET.get('nombre_places', '').strip()
    driver_verifie = request.GET.get('driver_verifie', 'off') == 'on'

    # Les deux lieux suffisent pour lancer une recherche ; les autres filtres restent facultatifs.
    if not point_depart or not destination:
        trips = trips.none()

    # Appliquer les filtres
    if point_depart:
        trips = trips.filter(route__point_depart__icontains=point_depart)

    if destination:
        trips = trips.filter(route__destination__icontains=destination)

    if date_depart:
        trips = trips.filter(date_depart=date_depart)

    if heure_depart:
        trips = trips.filter(heure_depart__gte=heure_depart)

    if prix_min:
        try:
            prix_min = int(prix_min)
            trips = trips.filter(prix_unitaire__gte=prix_min)
        except ValueError:
            pass

    if prix_max:
        try:
            prix_max = int(prix_max)
            trips = trips.filter(prix_unitaire__lte=prix_max)
        except ValueError:
            pass

    if nombre_places:
        try:
            nombre_places = int(nombre_places)
            trips = trips.filter(places_disponibles__gte=nombre_places)
        except ValueError:
            pass

    if driver_verifie:
        trips = trips.filter(driver__is_verified=True)

    # Éliminer les trajets complets
    trips = trips.exclude(places_disponibles=0)

    context = {
        'trips': trips,
        'routes': routes,
        'search_params': request.GET.dict(),
    }

    return render(request, 'search/search_trips.html', context)
