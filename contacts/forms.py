from django import forms
from .models import Entreprise, Agent
from django.forms.widgets import DateInput

class MessageForm(forms.Form):
    content = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Écris ton message ici...'}),
        max_length=100
    )

class EntrepriseForm(forms.ModelForm):
    date_creation = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        required=False
    )

    class Meta:
        model = Entreprise
        fields = ['nom', 'logo', 'nom_manager', 'adresse', 'telephone', 'site_web', 'email']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'nom_manager': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'site_web': forms.URLInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class AgentMinimalForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['prenom', 'nom']
        widgets = {
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
        }

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['prenom', 'nom', 'poste', 'email', 'telephone', 'photo', 'cv', 'date_naissance']
        widgets = {
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'poste': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cv': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_naissance': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
