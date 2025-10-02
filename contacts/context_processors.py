from .models import Entreprise

def entreprise_utilisateur(request):
    if request.user.is_authenticated:
        try:
            entreprise = Entreprise.objects.get(proprietaire=request.user)
            return {'mon_entreprise': entreprise}
        except Entreprise.DoesNotExist:
            return {'mon_entreprise': None}
    return {}
