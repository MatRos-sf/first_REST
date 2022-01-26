from django.contrib.auth.models import User
from rest_framework import viewsets, filters
from api.serializers import UserSerializer
from .models import Film, Recenzja, Aktor
from .serializers import FilmSerializer, FilmMiniSerializer, RecenzjaSerializer, AktorSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

from rest_framework.response import Response
from django.http.response import HttpResponseNotAllowed
from rest_framework.decorators import action
class FilmViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['tytul', 'opis','rok']        # nie używamy list wtedy

    search_fields = ['tytul', 'opis']               # /?serch=...

    def get_queryset(self):  # wyrzuca zawsze wieceeej niż jeden rekord wiec z get  wyskoczy błąd
        # rok =  self.request.query_params.get('rok', None)       # /filmy/?rok=2000
        # id = self.request.query_params.get('id', None )         # /filmy?rok=2000&id=2
        #
        #
        # if id:
        #     film = Film.objects.filter(id=id)
        #     return film
        # else:
        #     if rok:
        #         filmy = Film.objects.filter(rok=rok)
        #     else:
        #         filmy = Film.objects.all()
        #filmy = Film.objects.filter(po_premierze=True)
        filmy = Film.objects.all()
        return filmy

    # def list(self, request, *args, **kwargs):
    #     #queryset = self.get_queryset()
    #
    #     tytul = self.request.query_params.get('tytul', None)  # /filmy?rok=2000&id=2
    #     # more ->  https://docs.djangoproject.com/en/4.0/topics/db/queries/
    #     #film = Film.objects.filter(tytul__contains=tytul)      #tytul__exact tyt taki samy jaki w parametrach
    #                                                         #tytul__iexact nie jest wrażliwy na wielkość liter
    #     #film = Film.objects.filter(tytul__contains=tytul)      #tytul__contains czy podany string zawiera się w tyt
    #     #film = Film.objects.filter(premiera__gte="1800-01-01")      #lte i gte
    #     film = Film.objects.filter(premiera__year="2022")
    #
    #     serializer = FilmSerializer(film, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FilmSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        #czy użytkownik
        # if request.user.is_staff: #.is_superuser
        film = Film.objects.create(tytul = request.data['tytul'],
                                    opis = request.data['opis'],
                                    po_premierze = request.data['po_premierze'],
                                    rok = request.data['rok'])

        serializer = FilmSerializer(film, many=False)
        return Response(serializer.data)
        # else:
        #     return HttpResponseNotAllowed('Not allowed')

    def update(self, request, *args, **kwargs):
        film = self.get_object()
        film.tytul = request.data['tytul']
        film.opis = request.data['opis']
        film.po_premierze = request.data['po_premierze']
        film.rok = request.data['rok']
        film.save()

        serializer = FilmSerializer(film, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        film = self.get_object()
        film.delete()
        return Response("Film usuniety")

    @action(detail=True)        # true -> film/2/premiera - odnosi się do 1 rekordu
                                # false -> film/premiera
    def premiera(self, request, **kwargs):
        film = self.get_object()
        film.po_premierze = True
        film.save()
        serializer = FilmSerializer(film, many=False)
        return Response(serializer.data)

    @action(detail=True)
    def nopremiera(self,request, **kwargs):
        film = self.get_object()
        film.po_premierze = False
        film.save()
        serializer = FilmSerializer(film, many=False)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def premiera_wszystkie(self, request, **kwargs):
        filmy = Film.objects.all()
        filmy.update(po_premierze = request.data['po_premierze'])

        serializer = FilmSerializer(filmy, many=False)
        return Response(serializer.data)

    # @action(detail=False)
    # def przed_premiera_wszystkie(self, request, **kwargs):
    #     filmy = Film.objects.all()
    #     filmy.update(po_premierze=False)
    #
    #     serializer = FilmSerializer(filmy, many=False)
    #     return Response(serializer.data)


class RecenzjaViewSet(viewsets.ModelViewSet):

    queryset = Recenzja.objects.all()
    serializer_class = RecenzjaSerializer

class AktorViewSet(viewsets.ModelViewSet):

    queryset = Aktor.objects.all()
    serializer_class = AktorSerializer

    @action(detail=True, methods=['post'])
    def dolacz(self, request, **kwargs):
        aktor = self.get_object()
        film = Film.objects.get(id=request.data['film'])
        aktor.filmy.add(film)

        serializer = AktorSerializer(aktor, many=False)
        return Response(serializer.data)


