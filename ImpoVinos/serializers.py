from rest_framework import serializers
from .models import Vino, Categoria
import datetime

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']


class VinoSerializer(serializers.ModelSerializer):
    # 👇 Campos de solo lectura (derivados)
    categoria_id = serializers.IntegerField(source='categoria.id', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    # 👇 Campo de escritura para asignar categoría por id (opcional)
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
        help_text="ID de la categoría a asignar"
    )

    class Meta:
        model = Vino
        fields = [
            'id', 'nombre', 'pais_origen', 'anio', 'precio', 'stock',
            'categoria',          # write-only (entrada)
            'categoria_id',       # read-only (salida)
            'categoria_nombre'    # read-only (salida)
        ]

    # =====================
    # Validaciones de campo
    # =====================
    def validate_precio(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que cero.")
        return value

    def validate_stock(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value

    def validate_anio(self, value):
        current_year = datetime.date.today().year
        if value < 1900 or value > current_year:
            raise serializers.ValidationError(f"El año debe estar entre 1900 y {current_year}.")
        return value

    # =====================
    # Validación global
    # =====================
    def validate(self, attrs):
        nombre = attrs.get("nombre") or getattr(self.instance, "nombre", "")
        if not nombre or len(nombre.strip()) < 3:
            raise serializers.ValidationError({"nombre": "El nombre debe tener al menos 3 caracteres."})
        return attrs

    # =====================
    # Create / Update
    # =====================
    def create(self, validated_data):
        # Si viene 'categoria' en el payload, úsala; si no, deja la que tenga por defecto
        categoria = validated_data.pop('categoria', None)
        vino = Vino.objects.create(**validated_data)
        if categoria is not None:
            vino.categoria = categoria
            vino.save()
        return vino

    def update(self, instance, validated_data):
        categoria = validated_data.pop('categoria', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if categoria is not None:
            instance.categoria = categoria
        instance.save()
        return instance
