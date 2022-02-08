from django.contrib import admin
from .models import Usager, Alcool, DrinkHistorique, Drink


class UsagerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'nom', 'prenom', 'email', 'alcoolPref', 'id', )


class AlcoolAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id', )


class DrinkHistoriqueAdmin(admin.ModelAdmin):
    list_display = ('usager', 'drink', 'drink_id', 'date', 'id', )


class DrinkAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id', )


admin.site.register(Usager, UsagerAdmin)
admin.site.register(Alcool, AlcoolAdmin)
admin.site.register(DrinkHistorique, DrinkHistoriqueAdmin)
admin.site.register(Drink, DrinkAdmin)
