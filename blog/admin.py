# Dans le fichier admin.py
from django.contrib import admin
from .models import Article, Categorie, Commentaire

class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('contenu', 'auteur', 'article', 'date_creation')

class CommentaireInline(admin.TabularInline):
    model = Commentaire
    extra = 0

class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentaireInline]
    list_display = ('titre', 'categorie', 'date_creation', 'auteur', 'date_modification', 'nb_vues')
    list_filter = ('categorie','auteur',)
    search_fields = ('titre', 'contenu')

    ordering = ('-date_creation',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Categorie)
admin.site.register(Commentaire, CommentaireAdmin)
