from django.db import models
from django.utils import timezone
from datetime import timedelta

class Emprunt(models.Model):
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('retourne', 'Retourné'),
        ('en_retard', 'En retard'),
    ]

    utilisateur_id = models.IntegerField()
    livre_id = models.IntegerField()
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour_prevue = models.DateTimeField()
    date_retour_effective = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'emprunts'
        ordering = ['-date_emprunt']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_retour_prevue = timezone.now() + timedelta(days=14)
        # Mettre à jour le statut automatiquement
        if self.statut == 'en_cours' and timezone.now() > self.date_retour_prevue:
            self.statut = 'en_retard'
        super().save(*args, **kwargs)

    def est_en_retard(self):
        if self.statut == 'retourne':
            return False
        return timezone.now() > self.date_retour_prevue

    def jours_retard(self):
        if not self.est_en_retard():
            return 0
        delta = timezone.now() - self.date_retour_prevue
        return delta.days
