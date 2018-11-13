from django import forms
from .models import Idea, Comment

class IdeaForm(forms.ModelForm):

    class Meta:
        model = Idea
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('text', )