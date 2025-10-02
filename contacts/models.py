from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
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


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"De {self.sender.username} à {self.receiver.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
        
class Entreprise(models.Model):
    nom = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    nom_manager = models.CharField(max_length=255, blank=True)
    adresse = models.TextField(blank=True)
    site_web = models.URLField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    proprietaire = models.OneToOneField(User, on_delete=models.CASCADE)  # ✅ changement ici


class Agent(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='agents')
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    matricule = models.CharField(max_length=100, unique=True, blank=True)
    photo = models.ImageField(upload_to='photos_agents/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    poste = models.CharField(max_length=255, blank=True, null=True)
    cv = models.FileField(upload_to='cv_agents/', blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.matricule:
            total = Agent.objects.count() + 1
            self.matricule = f"AG-{total:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
