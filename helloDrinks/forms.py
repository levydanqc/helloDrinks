import datetime
import re
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

    def clean_nom(self):
        nom = self.cleaned_data['nom']
        if any(char.isdigit() for char in nom):
            raise forms.ValidationError(
                "Le nom ne peut pas contenir de chiffre.")
        return nom

    def clean_prenom(self):
        prenom = self.cleaned_data['prenom']
        if any(char.isdigit() for char in prenom):
            raise forms.ValidationError(
                "Le prénom ne peut pas contenir de chiffre.")
        return prenom

    def clean_email(self):
        email = self.cleaned_data['email']
        # check if email is valid
        if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("L'email n'est pas valide.")
        return email

    def clean_pseudo(self):
        pseudo = self.cleaned_data['pseudo']
        if Usager.objects.filter(pseudo=pseudo).exists():
            raise forms.ValidationError("Ce pseudo est déjà utilisé.")
        return pseudo

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError(
                "Le mot de passe doit contenir au moins 6 caractères.")
        return password

    def clean_adresse(self):
        adresse = self.cleaned_data['adresse']
        if not re.fullmatch(r"/[0-9]+[ |[a-zà-ú.,-]* ((autoroute)|(nord)|(sud)|(est)|(ouest)|(avenue)|(ruelle)|(rue)|(route)|(boulevard)|(rte)|(blvd\.)|(aut\.)|(ave\.)|)([ .,-]*[a-zà-ú0-9]*)*/i", adresse):
            raise forms.ValidationError("L'adresse n'est pas valide.")
        return adresse
    
    def clean_ddn(self):
        ddn = self.cleaned_data['ddn']
        if ddn > datetime.date.today():
            raise forms.ValidationError("La date de naissance n'est pas valide.")
        return ddn
    
    def clean_alcoolPref(self):
        alcoolPref = self.cleaned_data['alcoolPref']
        if not alcoolPref:
            raise forms.ValidationError("Veuillez choisir un alcool préféré.")
        return alcoolPref
