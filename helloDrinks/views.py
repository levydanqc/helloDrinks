import random
from datetime import datetime
from django.shortcuts import redirect, render
import urllib.parse
from .forms import UsagerForm
from .models import *
import requests
from django.contrib import messages


def index(request):
    if request.method == 'POST':
        form = UsagerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(usager, user=form.instance.id)
    else:
        form = UsagerForm()

    return render(request, 'helloDrinks/index.html', {'form': form})


def usager(request, user):
    if isinstance(user, int):
        usager = Usager.objects.get(id=user)
    else:
        usager = Usager.objects.get(pseudo=user)
    alcool = requests.get(
        "https://www.thecocktaildb.com/api/json/v1/1/search.php?i=%s" % usager.alcoolPref)
    ingredients = alcool.json()["ingredients"]
    thumbnail = requests.get(
        "https://www.thecocktaildb.com/images/ingredients/%s.png" % usager.alcoolPref)
    return render(request, 'helloDrinks/usager.html', {'usager': usager, 'ingredients': ingredients, "thumbnail": str(thumbnail.status_code)})


def choix(request, usager_id):
    usager = Usager.objects.get(id=usager_id)
    cocktails_api = requests.get(
        "http://www.thecocktaildb.com/api/json/v1/1/filter.php?i=%s" % urllib.parse.quote(usager.alcoolPref.nom))

    choix = []
    cocktails = []
    if len(cocktails_api.content):
        cocktails_api = cocktails_api.json()["drinks"]
        random.shuffle(cocktails_api)
        cocktails = cocktails_api.copy()
        for cocktail in cocktails_api:
            if len(cocktails) <= 3:
                break
            drink = Drink.objects.filter(nom=cocktail["strDrink"]).first()
            if drink and DrinkHistorique.objects.filter(drink=drink).exists():
                cocktails.remove(cocktail)

        if len(cocktails) > 3:
            cocktails = random.sample(cocktails, 3)
        for cocktail in cocktails:
            choix.append(requests.get(
                "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=%s" % urllib.parse.quote(cocktail["idDrink"])).json()["drinks"][0])

        for drink in choix:
            drink["ingredients"] = []
            for key, value in drink.items():
                if "strIngredient" in key and value:
                    drink["ingredients"].append({"ingredient": value, "mesure": drink.get(
                        "strMeasure" + key[-1])})

    response = render(request, 'helloDrinks/choixdrink.html',
                      {'cocktails': choix, 'usager': usager})
    response.set_cookie('nb_cocktails', len(cocktails_api))
    return response


def saveDrink(list):
    for cocktail in list:
        Drink.objects.get_or_create(nom=cocktail["strDrink"])


def saveOrder(request, usager, drink, unique):
    if not unique and DrinkHistorique.objects.filter(usager=usager).count() >= 5:
        DrinkHistorique.objects.filter(
            usager=usager).order_by('date').first().delete()
    elif unique and DrinkHistorique.objects.filter(usager=usager).exists():
        DrinkHistorique.objects.filter(
            usager=usager).first().delete()

    DrinkHistorique.objects.create(
        usager=usager, drink=drink, date=datetime.now())
    Drink.objects.get_or_create(nom=drink.nom)
    messages.add_message(request, messages.SUCCESS,
                         'Le kit %s a bien été commandé !' % drink.nom)


def order(request, usager_id, drink_name):
    nb_cocktails = request.COOKIES['nb_cocktails']
    usager = Usager.objects.get(id=usager_id)
    drink = Drink.objects.filter(nom=drink_name).first()

    if 4 <= int(nb_cocktails) <= 7:
        saveOrder(request, usager, drink, True)
    elif int(nb_cocktails) > 7:
        saveOrder(request, usager, drink, False)
    return redirect('choix', usager_id=usager_id)
