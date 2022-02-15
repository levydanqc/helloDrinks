import datetime
import re
from tabnanny import verbose
from django import forms
from .models import Usager


class UsagerForm(forms.Form):
    nom = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control my-2'}), required=False)
    prenom = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control my-2'}), required=False)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control my-2'}), required=False)
    pseudo = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control my-2'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control my-2'}), required=False)
    adresse = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control my-2'}), required=False)
    ddn = forms.CharField(widget=forms.DateInput(attrs={
        'class': 'form-control my-2', 'type': 'date'}), required=False, label="Date de naissance")
    alcoolPref = forms.CharField(widget=forms.Select(
        attrs={'class': 'form-control my-2'}), required=False, label="Alcool préféré")

    def clean_nom(self):
        nom = self.cleaned_data['nom']
        if nom == "":
            raise forms.ValidationError("Veuillez entrer votre nom.")
        if any(char.isdigit() for char in nom):
            raise forms.ValidationError(
                "Le nom ne peut pas contenir de chiffre.")
        return nom

    def clean_prenom(self):
        prenom = self.cleaned_data['prenom']
        if prenom == "":
            raise forms.ValidationError("Veuillez entrer votre prénom.")
        if any(char.isdigit() for char in prenom):
            raise forms.ValidationError(
                "Le prénom ne peut pas contenir de chiffre.")
        return prenom

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == "":
            raise forms.ValidationError("Veuillez entrer votre email.")
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("L'email n'est pas valide.")
        return email

    def clean_pseudo(self):
        pseudo = self.cleaned_data['pseudo']
        if pseudo == "":
            raise forms.ValidationError("Veuillez entrer votre pseudo.")
        if Usager.objects.filter(pseudo=pseudo).exists():
            raise forms.ValidationError("Ce pseudo est déjà utilisé.")
        return pseudo

    def clean_password(self):
        password = self.cleaned_data['password']
        if password == "":
            raise forms.ValidationError("Veuillez entrer votre mot de passe.")
        if len(password) < 6:
            raise forms.ValidationError(
                "Le mot de passe doit contenir au moins 6 caractères.")
        return password

    def clean_adresse(self):
        adresse = self.cleaned_data['adresse']
        if adresse == "":
            raise forms.ValidationError("Veuillez entrer votre adresse.")
        if re.fullmatch(r"/[0-9]+[ |[a-zà-ú.,-]* ((autoroute)|(nord)|(sud)|(est)|(ouest)|(avenue)|(ruelle)|(rue)|(route)|(boulevard)|(rte)|(blvd\.)|(aut\.)|(ave\.)|)([ .,-]*[a-zà-ú0-9]*)*/i", adresse):
            raise forms.ValidationError("L'adresse n'est pas valide.")
        return adresse

    def clean_ddn(self):
        ddn = self.cleaned_data['ddn']
        if ddn == "":
            raise forms.ValidationError(
                "Veuillez entrer votre date de naissance.")
        if ddn > datetime.date.today():
            raise forms.ValidationError(
                "La date de naissance n'est pas valide.")
        return ddn

    def clean_alcoolPref(self):
        alcoolPref = self.cleaned_data['alcoolPref']
        if alcoolPref == "":
            raise forms.ValidationError(
                "Veuillez entrer votre alcool préféré.")
        if not alcoolPref:
            raise forms.ValidationError("Veuillez choisir un alcool préféré.")
        return alcoolPref
