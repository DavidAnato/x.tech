from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['nom', 'email', 'numero_whatsapp', 'commentaire', 'photo', 'note']
        widgets = {
            'commentaire': forms.Textarea(attrs={'rows': 5}),
        }
