from django.db import models

class ExtraInfo(models.Model):
    RODZAJE = {
        (0, 'Nieznane'),
        (0, 'Horror'),
        (0, 'Sci-fi'),
        (0, 'Drama'),
        (0, 'Komedia')
    }
    czas_trwania = models.IntegerField()
    rodzaj = models.IntegerField(choices=RODZAJE, default=0)

class Film(models.Model):
    tytul = models.CharField(max_length= 32 )
    opis = models.TextField(max_length=256)
    po_premierze = models.BooleanField(default=False)
    premiera = models.DateField(null=True, blank=True)
    rok = models.IntegerField()
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=2,
                                      null=True, blank=True)
    extra_info = models.OneToOneField(ExtraInfo, on_delete=models.CASCADE,
                                      null=True, blank=True)

    def __str__(self):
        return self.moja_nazwa()

    def moja_nazwa(self):
        return f"{self.tytul} ( {str(self.rok)} )"

class Recenzja(models.Model):
    opis = models.TextField(default='')
    gwiazdki = models.IntegerField(default=5)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='recenzje')

class Aktor(models.Model):
    imie = models.CharField(max_length=32)
    nazwisko = models.CharField(max_length=32)
    filmy = models.ManyToManyField(Film)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"