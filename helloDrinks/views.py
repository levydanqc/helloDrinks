from django.shortcuts import redirect, render
from .forms import UsagerForm
from .models import Usager
# Create your views here.


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
    return render(request, 'helloDrinks/usager.html', {'usager': usager})
