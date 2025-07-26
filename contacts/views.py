from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Contact


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'contacts/signup.html', {'error': 'Les mots de passe ne correspondent pas.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'contacts/signup.html', {'error': 'Ce nom d’utilisateur existe déjà.'})

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect('accueil')

    return render(request, 'contacts/signup.html')

# contacts/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accueil')  # ou la page d’accueil de votre app
        else:
            return render(request, 'contacts/login.html', {'error': 'Identifiants invalides'})
    return render(request, 'contacts/login.html')


@login_required(login_url='login')
def accueil(request):
    return render(request, 'contacts/accueil.html')


@login_required(login_url='login')
def liste_contacts(request):
    if request.user.is_staff:
        contacts = Contact.objects.all()
    else:
        contacts = Contact.objects.filter(user=request.user)
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

        if Contact.objects.filter(user=request.user, prenom=prenom, nom=nom, telephone=telephone, email=email).exists():
            erreur = "Ce contact existe déjà."
        else:
            Contact.objects.create(
                user=request.user,
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

    if contact.user != request.user and not request.user.is_staff:
        return redirect('liste_contacts')

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

    if contact.user != request.user and not request.user.is_staff:
        return redirect('liste_contacts')

    if request.method == 'POST':
        contact.delete()
        return redirect('liste_contacts')

    return render(request, 'contacts/supprimer_contact.html', {'contact': contact})


@login_required(login_url='login')
def details_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if contact.user != request.user and not request.user.is_staff:
        return redirect('liste_contacts')

    return render(request, 'contacts/details.html', {'contact': contact})


def logout_view(request):
    logout(request)
    return redirect('login')
