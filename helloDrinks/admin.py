from django.contrib import admin
from .models import Usager, Alcool, DrinkHistorique, Drink


class UsagerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'nom', 'prenom', 'email', 'alcoolPref')


class AlcoolAdmin(admin.ModelAdmin):
    list_display = ('nom',)


class DrinkHistoriqueAdmin(admin.ModelAdmin):
    list_display = ("usager", "drink", "date")


class DrinkAdmin(admin.ModelAdmin):
    list_display = ("nom",)


admin.site.register(Usager, UsagerAdmin)
admin.site.register(Alcool, AlcoolAdmin)
admin.site.register(DrinkHistorique, DrinkHistoriqueAdmin)
admin.site.register(Drink, DrinkAdmin)
