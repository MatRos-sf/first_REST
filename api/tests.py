from django.test import TestCase
from .models import Film, Recenzja

# Create your tests here.

class FilmTestCase(TestCase):
    def setUp(self):
        Film.objects.create(tytul = "TestFilm", opis = "TestOpis", rok = 1, po_premierze= True)
        Film.objects.create(tytul = "TestFilm2", opis = "TestOpis2", rok = 2)

    def test_film_count(self):
        film_count = Film.objects.all().count()
        self.assertEqual(film_count, 2)

    def test_film_str(self):
        fOne = Film.objects.get(tytul = "TestFilm")
        self.assertEqual(fOne.moja_nazwa(), "TestFilm ( 1 )")

    def test_extra_info(self):
        fOne = Film.objects.get(id=1)
        self.assertEqual(fOne.extra_info, None)

    def test_change(self):
        fOne = Film.objects.get(tytul = "TestFilm")
        fOne.rok = 2
        fOne.save()
        self.assertEqual(fOne.rok, 2)

    def test_data(self):
        # trzeba będzie zrboić rok >= 1895
        fOne = Film.objects.get(tytul = "TestFilm")
        fOne.rok = -2
        fOne.save()
        self.assertEqual(fOne.rok, -2)

    def test_delet(self):
        Film.objects.get(id=1).delete()
        Film.objects.get(id=2).delete()
        film_count = Film.objects.all().count()
        self.assertEqual(film_count, 0, msg=f"Jest {film_count}")

    def test_IMBD(self):
        film = Film.objects.get(id=1)
        film.imdb_rating = 3
        film.save()
        self.assertEqual(film.imdb_rating, 3)

from rest_framework.test import APIRequestFactory, APITestCase

# class FilmTestClass(APITestCase):
#     def setUp(self):
#         factory = APIRequestFactory()
#         context = {
#             "tytul": "Matrix",
#             "opis": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence",
#             "po_premierze": True,
#             "rok": 1999
#         }
#         request = factory.post('/api/filmy/', context)
#         print(request)

from pytest_django.asserts import assertTemplateUsed

