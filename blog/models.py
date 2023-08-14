#models.py

from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    nb_vues = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='media/')
    auteur = models.CharField(max_length=200)

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ['-date_creation']

    @property
    def nb_commentaires(self):
        return self.commentaire_set.count()


class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    auteur = models.CharField(max_length=200)
    
    def __str__(self):
        return self.contenu[:50]
