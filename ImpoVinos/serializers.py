from rest_framework import serializers
from .models import Vino, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

class VinoSerializer(serializers.ModelSerializer):
    categoria_id = serializers.IntegerField(source='categoria.id', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Vino
        fields = [
            'id', 'nombre', 'pais_origen', 'anio', 'precio', 'stock',
            'categoria_id', 'categoria_nombre'
        ]