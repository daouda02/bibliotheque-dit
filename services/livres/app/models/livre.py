from django.db import models

class Livre(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    editeur = models.CharField(max_length=255, blank=True)
    annee_publication = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    nombre_exemplaires = models.IntegerField(default=1)
    exemplaires_disponibles = models.IntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'livres'
        ordering = ['titre']

    def __str__(self):
        return f"{self.titre} — {self.auteur}"

    def est_disponible(self):
        return self.exemplaires_disponibles > 0
