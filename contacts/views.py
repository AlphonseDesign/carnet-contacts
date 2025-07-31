from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Contact, Message
from .forms import MessageForm

# ✅ Fonction utilitaire pour ajouter unread_count
def get_unread_count(user):
    return Message.objects.filter(receiver=user, is_read=False).count()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accueil')
        else:
            return render(request, 'contacts/login.html', {'error': 'Identifiants invalides'})
    return render(request, 'contacts/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'registration/login.html', {'error': 'Les mots de passe ne correspondent pas.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'contacts/signup.html', {'error': 'Ce nom d’utilisateur existe déjà.'})

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect('accueil')

    return render(request, 'contacts/signup.html')

@login_required(login_url='login')
def accueil(request):
    unread_count = get_unread_count(request.user)
    return render(request, 'contacts/accueil.html', {'unread_count': unread_count})

@login_required(login_url='login')
def liste_contacts(request):
    contacts = Contact.objects.filter(utilisateur=request.user)
    unread_count = get_unread_count(request.user)
    return render(request, 'contacts/liste_contacts.html', {
        'contacts': contacts,
        'unread_count': unread_count
    })

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

        if Contact.objects.filter(prenom=prenom, nom=nom, telephone=telephone, email=email, utilisateur=request.user).exists():
            erreur = "Ce contact existe déjà."
        else:
            Contact.objects.create(
                utilisateur=request.user,
                prenom=prenom,
                nom=nom,
                telephone=telephone,
                email=email,
                adresse=adresse,
                genre=genre,
                photo=photo
            )
            return redirect('liste_contacts')

    unread_count = get_unread_count(request.user)
    return render(request, 'contacts/ajouter_contact.html', {'erreur': erreur, 'unread_count': unread_count})

@login_required(login_url='login')
def modifier_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, utilisateur=request.user)

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

    unread_count = get_unread_count(request.user)
    return render(request, 'contacts/modifier_contact.html', {'contact': contact, 'unread_count': unread_count})

@login_required(login_url='login')
def supprimer_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, utilisateur=request.user)

    if request.method == 'POST':
        contact.delete()
        return redirect('liste_contacts')

    unread_count = get_unread_count(request.user)
    return render(request, 'contacts/supprimer_contact.html', {'contact': contact, 'unread_count': unread_count})

@login_required(login_url='login')
def details(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, utilisateur=request.user)
    unread_count = get_unread_count(request.user)
    return render(request, 'contacts/details.html', {'contact': contact, 'unread_count': unread_count})

@user_passes_test(lambda u: u.is_superuser)
def liste_utilisateurs(request):
    utilisateurs = User.objects.all()
    unread_count = get_unread_count(request.user)
    return render(request, 'contacts/liste_utilisateurs.html', {
        'utilisateurs': utilisateurs,
        'unread_count': unread_count
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user)
    unread_count = get_unread_count(request.user)
    return render(request, 'messagerie/inbox.html', {
        'messages': messages,
        'unread_count': unread_count
    })

@login_required
def conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return redirect('conversation', username=other_user.username)

    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    unread_count = get_unread_count(request.user)

    return render(request, 'messagerie/conversation.html', {
        'messages': messages,
        'other_user': other_user,
        'unread_count': unread_count
    })

@user_passes_test(lambda u: u.is_superuser)
@login_required
def envoyer_message(request, username):
    destinataire = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                sender=request.user,
                receiver=destinataire,
                content=form.cleaned_data['content']
            )
            return redirect('inbox')
    else:
        form = MessageForm()

    unread_count = get_unread_count(request.user)
    return render(request, 'messagerie/envoyer_message.html', {
        'form': form,
        'destinataire': destinataire,
        'unread_count': unread_count
    })
