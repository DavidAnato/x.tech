#views.py

from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
from blog.models import Article
import json

# Create your views here.

def index(request):
    product_promo = Product.objects.filter(prix_promo__isnull=False)
    product_object = Product.objects.filter(categories__name='PC')
    nouveautes = Product.objects.filter(keywords__icontains='nouveauté')

    articles_list = Article.objects.order_by('-date_creation')
    comments = Comment.objects.all()

    return render(request, 'shop/index.html', {
        'product_object' : product_object,
        'articles' : articles_list,
        'product_promo': product_promo,
        'comments' : comments,
        'nouveautes': nouveautes 
    })



def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    return render(request, 'shop/detail.html', {'product': product_object})

def produit(request):
    product_object = Product.objects.order_by('-date_add')
    categories = Category.objects.all()
    types = Type.objects.all()
    item_name = request.GET.get('item-name')

    if item_name:
        product_object = product_object.filter(
            Q(title__icontains=item_name) |
            Q(categories__name__icontains=item_name) |
            Q(keywords__icontains=item_name) |
            Q(marque__icontains=item_name) |
            Q(type__name__icontains=item_name) |
            Q(processeur__icontains=item_name) |
            Q(taille__icontains=item_name) 
        )

    if not product_object:
        return redirect('produit')

    return render(request, 'shop/produit.html', {'product_object': product_object, 'categories': categories, 'types': types})


def panier(request):
    codes = CodePromo.objects.filter(valide=True)
    panier = json.loads(request.session.get('panier', '{}'))
    total = 0
    panier_products = []
    for id, qty in panier.items():
        product = Product.objects.get(id=id)
        if product.prix_promo:
            prix = product.prix_promo
        else:
            prix = product.prix
        total += prix * qty
        panier_products.append({
            'id': id,
            'title': product.title,
            'qty': qty,
            'prix': prix
        })
    return render(request, 'panier.html', {'panier_products': panier_products, 'codes': codes, 'total': total})


def add_to_panier(request, id):
    panier = json.loads(request.session.get('panier', '{}'))
    panier[id] = 1
    request.session['panier'] = json.dumps(panier)
    return redirect('panier')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def remove_from_panier(request, id):
    panier = json.loads(request.session.get('panier', '{}'))
    if str(id) in panier:
        del panier[str(id)]
        request.session['panier'] = json.dumps(panier)
    return redirect('panier')

def clear_panier(request):
    request.session['panier'] = json.dumps({})
    # return redirect('panier')


from django.shortcuts import render, redirect
from .models import Order

def order(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        prenoms = request.POST['prenoms']
        email = request.POST['email']
        whatsapp = request.POST['whatsapp']
        address = request.POST['address']
        screenshot = request.POST['screenshot'] 

        order = Order(nom=nom, prenoms=prenoms, email=email, whatsapp=whatsapp, address=address, screenshot=screenshot)
        order.save()
        clear_panier(request)
        return render(request, 'order.html')

def service(request):
    return render(request, 'shop/service.html')

from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm

def comments(request):
    commentaires = Comment.objects.filter(approuve=True).order_by('-date_ajout')
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('comments')
    context = {
        'commentaires': commentaires,
        'form': form,
    }
    return render(request, 'shop/comments.html', context)

def handler404(request, exception):
    return render(request, '404.html')