from django.db import migrations

def crear_categorias_iniciales(apps, schema_editor):
    Categoria = apps.get_model('ImpoVinos', 'Categoria')
    
    # Intenta obtener la categoría 'Nacional', si no existe, la crea
    Categoria.objects.get_or_create(nombre='Nacional')

    # Intenta obtener la categoría 'Importado', si no existe, la crea
    Categoria.objects.get_or_create(nombre='Importado')

class Migration(migrations.Migration):

    dependencies = [
        ('ImpoVinos', '0001_initial'),  # Asegúrate que este sea el nombre de tu migración anterior
    ]

    operations = [
        migrations.RunPython(crear_categorias_iniciales),
    ]