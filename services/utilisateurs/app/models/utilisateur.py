from django.db import models

class Utilisateur(models.Model):
    TYPE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('professeur', 'Professeur'),
        ('personnel', 'Personnel'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    type_utilisateur = models.CharField(max_length=20, choices=TYPE_CHOICES, default='etudiant')
    numero_carte = models.CharField(max_length=50, unique=True)
    actif = models.BooleanField(default=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'utilisateurs'
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.type_utilisateur})"

    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
