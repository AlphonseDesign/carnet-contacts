from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [ 
    path('', views.login_view, name='login'),  # Page principale
    path('accueil/', views.accueil, name='accueil'),
    path('logout/', views.logout_view, name='logout'),
    path('contacts/', views.liste_contacts, name='liste_contacts'),
    path('ajouter/', views.ajouter_contact, name='ajouter_contact'),
    path('modifier/<int:contact_id>/', views.modifier_contact, name='modifier_contact'),
    path('supprimer/<int:contact_id>/', views.supprimer_contact, name='supprimer_contact'),
    path('contact/<int:contact_id>/', views.details_contact, name='detail_contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
