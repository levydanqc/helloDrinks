import random
from datetime import datetime
from django.shortcuts import redirect, render
from matplotlib.image import thumbnail
from .forms import UsagerForm
from .models import DrinkHistorique, Usager, Drink
import requests


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
    cocktails = requests.get(
        "http://www.thecocktaildb.com/api/json/v1/1/filter.php?i=%s" % usager.alcoolPref.nom).json()["drinks"]

    list = []
    # if len(cocktails) <= 0:
    #     for cocktail in cocktails:
    #         drink = Drink.objects.filter(nom=cocktail["strDrink"]).first()
    #         if drink and DrinkHistorique.objects.filter(drink=drink.id).exists():
    #             cocktails.remove(cocktail)

    #     for cocktail in random.sample(cocktails, 3):
    #         list.append(requests.get(
    #             "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=%s" % cocktail["idDrink"]).json()["drinks"][0])

    #     saveToDb(usager, list)

    return render(request, 'helloDrinks/choixdrink.html', {'cocktails': list})


def saveToDb(usager, list):
    for cocktail in list:
        drink = Drink.objects.get_or_create(nom=cocktail["strDrink"])
        DrinkHistorique.objects.create(
            usager=usager, drink=drink[0], date=datetime.now())
