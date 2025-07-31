from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [ 
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('accueil/', views.accueil, name='accueil'),
    path('contacts/', views.liste_contacts, name='liste_contacts'),
    path('ajouter/', views.ajouter_contact, name='ajouter_contact'),
    path('modifier/<int:contact_id>/', views.modifier_contact, name='modifier_contact'),
    path('supprimer/<int:contact_id>/', views.supprimer_contact, name='supprimer_contact'),
    path('contact/<int:contact_id>/', views.details, name='details'),
    path('inbox/', views.inbox, name='inbox'),
    path('messages/<str:username>/', views.conversation, name='conversation'),
    path('utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('message/envoyer/<str:username>/', views.envoyer_message, name='envoyer_message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
