import random
from datetime import datetime
from django.shortcuts import redirect, render
from matplotlib.image import thumbnail
from .forms import UsagerForm
from .models import *
import requests
from django.contrib import messages


def index(request):
    if request.method == 'POST':
        form = UsagerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(usager, usager_id=form.instance.id)
    else:
        form = UsagerForm()

    return render(request, 'helloDrinks/index.html', {'form': form})


def usager(request, usager_id):
    usager = Usager.objects.get(id=usager_id)
    alcool = requests.get(
        "https://www.thecocktaildb.com/api/json/v1/1/search.php?i=%s" % usager.alcoolPref)
    ingredients = alcool.json()["ingredients"]
    thumbnail = requests.get(
        "https://www.thecocktaildb.com/images/ingredients/%s.png" % usager.alcoolPref)
    return render(request, 'helloDrinks/usager.html', {'usager': usager, 'ingredients': ingredients, "thumbnail": str(thumbnail.status_code)})


def choixDrink(request, usager_id):
    usager = Usager.objects.get(id=usager_id)
    cocktails_api = requests.get(
        "http://www.thecocktaildb.com/api/json/v1/1/filter.php?i=%s" % usager.alcoolPref.nom).json()["drinks"]

    random.shuffle(cocktails_api)
    cocktails = cocktails_api.copy()
    choix = []
    if len(cocktails) > 0:
        for cocktail in cocktails_api:
            if len(cocktails) <= 3:
                break
            drink = Drink.objects.filter(nom=cocktail["strDrink"]).first()
            if drink and DrinkHistorique.objects.filter(drink=drink).exists():
                cocktails.remove(cocktail)

        if len(cocktails) > 3:
            for cocktail in random.sample(cocktails, 3):
                choix.append(requests.get(
                    "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=%s" % cocktail["idDrink"]).json()["drinks"][0])
        else:
            choix = cocktails

        saveDrink(choix)

    return render(request, 'helloDrinks/choixdrink.html', {'cocktails': choix, 'usager': usager})


def saveDrink(list):
    for cocktail in list:
        Drink.objects.get_or_create(nom=cocktail["strDrink"])


def saveOrder(request, usager, drink):
    if DrinkHistorique.objects.filter(usager=usager).count() >= 5:
        oldest = DrinkHistorique.objects.filter(
            usager=usager).order_by('date').first()
        oldest.delete()
    DrinkHistorique.objects.create(
        usager=usager, drink=drink, date=datetime.now())
    messages.add_message(request, messages.SUCCESS,
                         'Le kit %s a bien été commandé !' % drink.nom)


def order(request, usager_id, drink_name):
    usager = Usager.objects.get(id=usager_id)
    drink = Drink.objects.filter(nom=drink_name).first()
    saveOrder(request, usager, drink)
    return redirect('choixDrink', usager_id=usager_id)
