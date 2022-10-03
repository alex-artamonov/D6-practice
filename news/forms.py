# from django.forms import ModelForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import Post
from django import forms


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'content', 'type', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows':10, 'placeholder': '{скопируй текст ниже, если нечего сказать}' }),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user