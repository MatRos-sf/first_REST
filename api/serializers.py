from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Film, ExtraInfo, Recenzja, Aktor

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')

class ExtraInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraInfo
        fields = '__all__'

class RecenzjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recenzja
        #fields = ('id','tytul', 'opis', 'po_premierze', 'premiera', 'rok', 'extra_info')
        #fields = ('opis', 'gwiazdki')
        fields = '__all__'
        # depth = 1       #jak gł
        # #exclude - > co nie
        def update(self, instance, validated_data): # bez read_only
            instance.opis = validated_data.get('opis', instance.opis)           #  jeżeeli niee zostaną podane zmieniamy na instance.opis czyli to co był o
            instance.gwiazdki = validated_data.get('gwiazdki', instance.gwiazdki)
            instance.save()

            return instance



class FilmSerializer(serializers.ModelSerializer):
    extra_info = ExtraInfoSerializer(many=False)
    recenzje = RecenzjaSerializer(many=True)
    class Meta:
        model = Film
        fields = ('id','tytul', 'opis', 'po_premierze', 'premiera', 'rok', 'extra_info','recenzje' )
        #fields = '__all__'
        read_only_fileds = ('extra_info','recenzje',)

class FilmMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('tytul', 'rok')

class AktorSerializer(serializers.ModelSerializer):
    filmy = FilmMiniSerializer(many=True, read_only=True)
    class Meta:
        model = Aktor
        fields = ('id','imie', 'nazwisko', 'filmy')

    # def create(self, validated_data): # bez read_only
    #     filmy = validated_data["filmy"]
    #     del validated_data["filmy"]
    #
    #     aktor = Aktor.objects.create(**validated_data)
    #
    #     for film in filmy:
    #         f = Film.objects.create(**film)
    #         aktor.filmy.add(f)
    #
    #     aktor.save()
    #     return aktor


