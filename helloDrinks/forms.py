from django import forms
from .models import Usager


class UsagerForm(forms.ModelForm):
    class Meta:
        model = Usager
        fields = ['email', 'nom', 'prenom', 'pseudo', 'password',
                  'adresse', 'ddn', 'alcoolPref']
        labels = {'ddn': 'Date de naissance'}
        help_texts = {'ddn': 'Veuillez entrer votre date de naissance'}
