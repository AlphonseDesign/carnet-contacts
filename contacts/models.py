from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Lien avec utilisateur
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    genre = models.CharField(
        max_length=1,
        choices=[('M', 'Masculin'), ('F', 'Féminin')],
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.prenom} {self.nom}"
