#urls.py
from django.contrib import admin
from django.urls import path
from . import views

handler404 = 'shop.views.handler404'

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:myid>', views.detail, name = 'detail'),
    path('produit/', views.produit, name = 'produit'),

    path('panier/', views.panier, name='panier'),
    path('panier/add/<int:id>/', views.add_to_panier, name='add_to_panier'),
    path('remove/<int:id>/', views.remove_from_panier, name='remove_from_panier'),
    path('clear/', views.clear_panier, name='clear_panier'),

    
    path('order/', views.order, name='order'),
    
    path('nos_service/', views.service, name = 'service'),

    path('comments/', views.comments, name='comments'),

    path('admin/', admin.site.urls),

]