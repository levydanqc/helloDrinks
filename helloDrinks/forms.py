from django import forms
from .models import Usager


class UsagerForm(forms.ModelForm):
    class Meta:
        model = Usager
        # fields = ['email', 'nom', 'prenom', 'pseudo', 'password',
        #           'adresse', 'ddn', 'alcoolPref']
        labels = {'ddn': 'Date de naissance', "alcoolPref": "Alcool préféré"}
        # help_texts = {'ddn': 'Veuillez entrer votre date de naissance'}
        fields = "__all__"
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'email': forms.EmailInput(attrs={'class': 'form-control my-2'}),
            'pseudo': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control my-2'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'ddn': forms.DateInput(attrs={'class': 'form-control my-2', 'type': 'date'}),
            'alcoolPref': forms.Select(attrs={'class': 'form-control my-2'}),
        }
