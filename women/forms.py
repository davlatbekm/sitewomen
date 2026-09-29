from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator

from .models import Category, Husband, Women


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category", widget=forms.Select(attrs={'class': 'form-control w-75'}))
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(),  required=False, empty_label="Single", widget=forms.Select(attrs={'class': 'form-control w-75'}))

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control w-75'}),
            'slug': forms.TextInput(attrs={'class': 'form-control w-75' }),
            'content': forms.Textarea(attrs={'class': 'form-control w-75', "rows":5 }),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control w-75'}),
        }
        labels = {
            'slug':'URL'
        }

class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Upload File", widget=forms.FileInput(attrs={'class': 'form-control w-75'}))



class WomenUpdateForm(forms.ModelForm):
    class Meta:
        model = Women
        fields = ['title', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control w-75'}),
            'content': forms.Textarea(attrs={'class': 'form-control w-75', 'rows': 5}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control w-75'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cat': forms.Select(attrs={'class': 'form-select w-75'}),
        }
