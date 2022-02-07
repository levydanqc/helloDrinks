from random import random
from django.shortcuts import redirect, render
from matplotlib.image import thumbnail
from .forms import UsagerForm
from .models import Usager
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
        "www.thecocktaildb.com/api/json/v1/1/filter.php?i=%s" % usager.alcoolPref)
    choix = random.sample(cocktails.json()["drinks"], 3)
    return render(request, 'helloDrinks/choixdrink.html')
