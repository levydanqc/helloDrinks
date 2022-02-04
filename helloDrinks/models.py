from django.db import models

# Create your models here.


class Usager(models.Model):
    def __str__(self) -> str:
        return self.pseudo
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    ddn = models.DateField()
    pseudo = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    alcoolPref = models.ForeignKey('Alcool', on_delete=models.CASCADE)


class Alcool(models.Model):
    def __str__(self) -> str:
        return self.nom
    nom = models.CharField(max_length=50)


class DrinkHistorique(models.Model):
    def __str__(self) -> str:
        return '{} - {}'.format(self.usager, self.alcool)
    usager = models.ForeignKey(Usager, on_delete=models.CASCADE)
    alcool = models.ForeignKey(Alcool, on_delete=models.CASCADE)
    date = models.DateTimeField()


class Drink(models.Model):
    def __str__(self) -> str:
        return self.nom
    nom = models.CharField(max_length=50)
