from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Contact

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accueil')
        else:
            return render(request, 'contacts/login.html', {'error': 'Nom d’utilisateur ou mot de passe incorrect'})
    
    return render(request, 'contacts/login.html')


@login_required(login_url='login')
def accueil(request):
    return render(request, 'contacts/accueil.html')

def liste_contacts(request):
    contacts = Contact.objects.all()
    return render(request, 'contacts/liste_contacts.html', {'contacts': contacts})

@login_required(login_url='login')
def ajouter_contact(request):
    erreur = None
    if request.method == 'POST':
        prenom = request.POST.get('prenom', '').strip()
        nom = request.POST.get('nom', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        email = request.POST.get('email', '').strip()
        adresse = request.POST.get('adresse', '').strip()
        genre = request.POST.get('genre')
        photo = request.FILES.get('photo')

        if Contact.objects.filter(prenom=prenom, nom=nom, telephone=telephone, email=email).exists():
            erreur = "Ce contact existe déjà."
        else:
            Contact.objects.create(
                prenom=prenom,
                nom=nom,
                telephone=telephone,
                email=email,
                adresse=adresse,
                genre=genre,
                photo=photo
            )
            return redirect('liste_contacts')

    return render(request, 'contacts/ajouter_contact.html', {'erreur': erreur})

@login_required(login_url='login')
def modifier_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        contact.prenom = request.POST.get('prenom', '').strip()
        contact.nom = request.POST.get('nom', '').strip()
        contact.telephone = request.POST.get('telephone', '').strip()
        contact.email = request.POST.get('email', '').strip()
        contact.adresse = request.POST.get('adresse', '').strip()
        contact.genre = request.POST.get('genre')

        if request.FILES.get('photo'):
            contact.photo = request.FILES['photo']

        contact.save()
        return redirect('liste_contacts')

    return render(request, 'contacts/modifier_contact.html', {'contact': contact})

@login_required(login_url='login')
def supprimer_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        contact.delete()
        return redirect('liste_contacts')

    return render(request, 'contacts/supprimer_contact.html', {'contact': contact})

@login_required(login_url='login')
def details_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    return render(request, 'contacts/details.html', {'contact': contact})

def logout_view(request):
    logout(request)
    return redirect('login')
