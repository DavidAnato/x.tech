from django.contrib import admin
from .models import *

# Register your models here.
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'date_added')

class AdminType(admin.ModelAdmin):
    list_display = ('name', 'date_added')

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class AdminProduct(admin.ModelAdmin):
    list_filter = ('categories', 'type',)
    inlines = [ProductImageInline]
    list_display = ['title', 'prix', 'prix_promo', 'date_add']
    fieldsets = (
        (None, {
            'fields': ('title', 'prix', 'prix_promo', 'description', 'categories', 'type', 'marque', 'processeur', 'taille', 'keywords', 'image')
        }),
    )

class AdminOrder(admin.ModelAdmin):
    list_filter = ('livree',)
    list_display = ['id','nom', 'prenoms', 'whatsapp','address', 'date_created', 'image_tag', 'livree']

class AdminCodePromo(admin.ModelAdmin):
    list_display = ['code', 'reduction','valide',]
    list_filter = ('valide',)

class AdminComment(admin.ModelAdmin):
    list_filter = ('approuve',)

admin.site.register(Comment, AdminComment)
admin.site.register(Order, AdminOrder)
admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(Type, AdminType)
admin.site.register(CodePromo, AdminCodePromo)
