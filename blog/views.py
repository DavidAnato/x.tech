#views.py
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import F
from .models import Article, Categorie, Commentaire


def articles(request):
    articles_list = Article.objects.order_by('-date_creation')
    categories_list = Categorie.objects.all()

    # Trie les articles par catégorie si le paramètre "categorie" est présent dans la requête
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        articles_list = articles_list.filter(categorie=categorie_id)

    # Traitement des nb_vues
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article = get_object_or_404(Article, pk=article_id)
        article.nb_vues = F('nb_vues') + 1
        article.save()

    context = {
        'articles': articles_list,
        'categories': categories_list,
    }
    
    return render(request, 'blog/articles.html', context)



def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    articles_recents = Article.objects.order_by('-date_creation')
    commentaires = article.commentaire_set.all()

    # Traitement des commentaires
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        auteur = request.POST.get('auteur')
        commentaire = Commentaire(article=article, auteur=auteur, contenu=contenu, date_creation=timezone.now())
        commentaire.save()

    # Formatage du nombre de nb_vues
    nb_vues = article.nb_vues
    if nb_vues >= 1000000:
        nb_vues = str(round(nb_vues/1000000, 1)) + 'M'
    elif nb_vues >= 1000:
        nb_vues = str(round(nb_vues/1000, 1)) + 'k'
    else:
        nb_vues = str(nb_vues)

    context = {
        'article': article,
        'nb_vues': nb_vues,
        'commentaires': commentaires,
        'articles_recents': articles_recents
    }

    return render(request, 'blog/article_detail.html', context)
