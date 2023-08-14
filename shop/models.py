#models.py
import random
from datetime import timedelta

from django.db import models
from django.utils.html import format_html
from django.utils import timezone

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageDraw, ImageFont


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-date_added']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name  

class Type(models.Model):
    name = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-date_added']
        verbose_name_plural = "Types"

    def __str__(self):
        return self.name 
    
class Product(models.Model):
    title = models.CharField(max_length=200)
    prix = models.FloatField()
    prix_promo = models.FloatField(null=True, blank=True)
    description = models.TextField()
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')
    keywords = models.CharField(max_length=200)
    marque = models.CharField(max_length=100, null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    processeur = models.CharField(max_length=100, null=True, blank=True)
    taille = models.CharField(max_length=100, null=True, blank=True)

    date_add = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_add']
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(upload_to='media/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='other_images')
    class Meta:
        verbose_name_plural = "Images Produits"

from django.db import models
from django.utils import timezone

from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class CodePromo(models.Model):
    code = models.CharField(max_length=100)
    reduction = models.FloatField()
    valide = models.BooleanField(default=True)
    date_debut = models.DateTimeField(default=timezone.now)
    date_fin = models.DateTimeField(default=timezone.now() + timedelta(days=7))

    class Meta:
        verbose_name_plural = "Codes Promo"

    def auto_save(self, *args, **kwargs):
        now = timezone.now()
        if self.date_debut <= now <= self.date_fin:
            self.valide = True
        else:
            self.valide = False

    def save(self, *args, **kwargs):
        self.auto_save()
        super().save(*args, **kwargs)

@receiver(pre_save, sender=CodePromo)
def pre_save_codepromo(sender, instance, **kwargs):
    if instance.pk:
        # On vérifie que l'instance existe déjà en base de données
        old_instance = CodePromo.objects.get(pk=instance.pk)
        if old_instance.date_debut != instance.date_debut or old_instance.date_fin != instance.date_fin:
            # Si les dates ont été modifiées, on appelle la méthode auto_save
            instance.auto_save()

@receiver(post_save, sender=CodePromo)
def post_save_codepromo(sender, instance, **kwargs):
    if not instance.pk:
        # Si l'instance est nouvellement créée, on appelle la méthode auto_save
        instance.auto_save()


class Order(models.Model):
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=20)
    address = models.TextField()
    screenshot = models.TextField()
    livree = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    def image_tag(self):
        return format_html('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"><script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script><button type="button" data-toggle="modal" data-target="#myModal{}"><img src="{}" width="50" height="50"/></button><div class="modal fade" id="myModal{}" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-body"><img src="{}" width="100%" height="100%"/></div></div></div></div>'.format(self.id, self.screenshot, self.id, self.screenshot))

    image_tag.short_description = 'Image'
    class Meta:
        verbose_name_plural = "Commandes"

class Comment(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    numero_whatsapp = models.CharField(max_length=15)
    commentaire = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    admin_reponse = models.TextField(blank=True, null=True)
    approuve = models.BooleanField(default=True)
    note = models.IntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])
    date_ajout = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nom} - {self.commentaire[:50]}"

    def save(self, *args, **kwargs):
        if not self.photo: # Si le champ photo est vide
            # Création de l'image
            size = (280, 280)
            image = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("arialbd.ttf", 170)  # Police Arial Black, taille 128
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Couleur de police aléatoire
            img = ''
            txt = self.nom.split()
            
            for word in txt:
                    img += word[0]
                    if len(img) == 2:
                        break

            draw.text((25, 45), img.upper(), fill=color, font=font)

            # Enregistrement de l'image dans le champ photo
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)
            self.photo = InMemoryUploadedFile(buffer, 'ImageField', f"{self.nom[0].upper()}.png", 'image/png', buffer.getbuffer().nbytes, None)
            
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Commentaires"
