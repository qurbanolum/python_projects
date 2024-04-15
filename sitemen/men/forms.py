from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator

from .models import Category, Wife, Men


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Category not chosen', label='Category')
    wife = forms.ModelChoiceField(queryset=Wife.objects.all(), empty_label='Not married', required=False)

    class Meta:
        model = Men
        fields = ['title', 'slug', 'photo', 'content', 'is_published', 'cat', 'wife', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {'slug': 'URL'}


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=255)
    email = forms.EmailField(label='E-mail')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))


class UploadFileForm(forms.Form):
    file = forms.FileField(label='File')
