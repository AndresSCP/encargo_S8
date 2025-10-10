from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Vino, Categoria, Usuario, Cliente
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import VinoSerializer
import re

# Create your views here.

# Home / landing page
def index(request):
    return render(request, "index.html")

# Interacciones (nuevamente, se puede cambiar el nombre de esta folder)
def comprar(request):
    return render(request, "interacciones/comprar.html")

def nosotros(request):
    return render(request, "interacciones/nosotros.html")

def contacto(request):
    return render(request, "interacciones/contacto.html")

def carrito(request):
    return render(request, "interacciones/carrito.html")

# Productos
def prod_nacionales(request):
    # Obtener la categoría "Nacional" de la base de datos
    categoria_nacional = Categoria.objects.get(nombre='Nacional')
    # Filtrar los vinos por esa categoría
    vinos_nacionales = Vino.objects.filter(categoria=categoria_nacional)
    # Pasar los vinos a la plantilla
    return render(request, "productos/nacionales.html", {'vinos': vinos_nacionales})

def prod_importados(request):
    # Obtener la categoría "Importado" de la base de datos
    categoria_importado = Categoria.objects.get(nombre='Importado')
    # Filtrar los vinos por esa categoría
    vinos_importados = Vino.objects.filter(categoria=categoria_importado)
    # Pasar los vinos a la plantilla
    return render(request, "productos/importados.html", {'vinos': vinos_importados})

# Usuarios
def ingresa(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        correo = request.POST.get('correo')
        clave = request.POST.get('clave')

        # Autenticar al usuario
        user = authenticate(request, username=correo, password=clave)
        
        if user is not None:
            # Si el usuario es válido, iniciar sesión
            login(request, user)
            messages.success(request, '¡Has iniciado sesión correctamente!')
            return redirect('index')

        else:
            # Si el usuario no es válido, mostrar un error
            messages.error(request, 'Correo o contraseña incorrectos.')
            return render(request, "usuarios/ingresa.html")
            
    else:
        # Si la solicitud es GET, simplemente muestra la página de ingreso
        return render(request, "usuarios/ingresa.html")

from django.contrib.auth.hashers import make_password
from .models import Usuario, Cliente
import re

def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        clave = request.POST.get('clave')
        clave2 = request.POST.get('clave2')

        # Validación 1: Las contraseñas deben coincidir
        if clave != clave2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, "usuarios/registro.html")

        # Validación 2: Longitud mínima de 8 caracteres
        if len(clave) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, "usuarios/registro.html")

        # Validación 3: Debe contener al menos una letra mayúscula
        if not re.search(r'[A-Z]', clave):
            messages.error(request, 'La contraseña debe contener al menos una letra mayúscula.')
            return render(request, "usuarios/registro.html")

        # Validación 4: Debe contener al menos un número
        if not re.search(r'\d', clave):
            messages.error(request, 'La contraseña debe contener al menos un número.')
            return render(request, "usuarios/registro.html")

        # Validación 5: Debe contener al menos un carácter especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', clave):
            messages.error(request, 'La contraseña debe contener al menos un carácter especial (!@#$%^&*...).')
            return render(request, "usuarios/registro.html")

        # Validación 6: Longitud máxima de 128 caracteres
        if len(clave) > 128:
            messages.error(request, 'La contraseña no puede tener más de 128 caracteres.')
            return render(request, "usuarios/registro.html")

        # Verificar si el correo ya está registrado
        if User.objects.filter(username=correo).exists():
            messages.error(request, 'Este correo ya está registrado.')
            return render(request, "usuarios/registro.html")

        try:
            # Crear el usuario de Django (para autenticación)
            user = User.objects.create_user(
                username=correo,
                email=correo,
                password=clave,
                first_name=nombre
            )

            # Crear el usuario en tu modelo personalizado
            usuario = Usuario.objects.create(
                nombre=nombre,
                email=correo,
                password=make_password(clave),
                es_admin=False
            )

            # Crear el cliente asociado (con datos por defecto, puede actualizar después)
            Cliente.objects.create(
                usuario=usuario,
                direccion='',  # Se puede completar en modificar perfil
                telefono=''
            )

            # Iniciar sesión automáticamente después del registro
            user = authenticate(request, username=correo, password=clave)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {nombre}! Tu cuenta ha sido creada exitosamente.')
                return redirect('index')

        except Exception as e:
            messages.error(request, f'Error al crear la cuenta: {str(e)}')
            return render(request, "usuarios/registro.html")

    return render(request, "usuarios/registro.html")

def recuperar(request):
    return render(request, "usuarios/recuperar.html")

def perfil(request):
    return render(request, "usuarios/perfil.html")

def modificarPerfil(request):
    return render(request, "usuarios/modificarPerfil.html")

def ingresa_admin(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password') 

        user = authenticate(request, username=usuario, password=password)

        if user is not None:
            if user.is_superuser or user.is_staff:
                login(request, user)
                messages.success(request, '¡Has ingresado como administrador!')
                return redirect('index')
            else:
                messages.error(request, 'No tienes permisos de administrador.')
                return render(request, "usuarios/admin.html")
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, "usuarios/admin.html")
            
    return render(request, "usuarios/admin.html")

def es_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(es_admin, login_url='/usuarios/ingresa_admin/')
def Inventario(request):
    categorias = Categoria.objects.all()
    vinos = Vino.objects.all().order_by('nombre')

    if request.method == 'POST':
        # AGREGAR VINO
        if 'agregar' in request.POST:
            nombre = request.POST.get('producto')
            categoria_id = request.POST.get('categoria')
            stock = request.POST.get('cantidad')
            precio = request.POST.get('precio')
            pais = request.POST.get('pais')
            anio = request.POST.get('anio')

            try:
                categoria = Categoria.objects.get(id=categoria_id)
                Vino.objects.create(
                    nombre=nombre,
                    pais_origen=pais or "",
                    anio=anio or None,
                    precio=precio,
                    stock=stock,
                    categoria=categoria
                )
                messages.success(request, f"Vino '{nombre}' agregado correctamente.")
            except Categoria.DoesNotExist:
                messages.error(request, "La categoría seleccionada no existe.")
            
            return redirect('inventario')

        # ELIMINAR VINO / CANTIDAD
        elif 'eliminar' in request.POST:
            vino_id = request.POST.get('vino_id')
            cantidad = request.POST.get('cantidad')

            vino = get_object_or_404(Vino, id=vino_id)

            if cantidad:
                cantidad = int(cantidad)
                if cantidad >= vino.stock:
                    vino.delete()
                    messages.success(request, f"Vino '{vino.nombre}' eliminado completamente.")
                else:
                    vino.stock -= cantidad
                    vino.save()
                    messages.success(request, f"Se eliminaron {cantidad} unidades de '{vino.nombre}'.")
            else:
                vino.delete()
                messages.success(request, f"Vino '{vino.nombre}' eliminado completamente.")

            return redirect('inventario')

    contexto = {
        'vinos': vinos,
        'categorias': categorias
    }
    return render(request, "interacciones/Inventario.html", contexto)

@user_passes_test(es_admin, login_url='/usuarios/ingresa_admin/')
def eliminar_vino(request, vino_id):
    vino = get_object_or_404(Vino, id=vino_id)
    if request.method == 'POST':
        vino.delete()
    return redirect('inventario')


class VinoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VinoSerializer

    def get_queryset(self):
        qs = Vino.objects.all()
        order = self.request.query_params.get('order', '-id')
        # por seguridad dejamos ordenamientos permitidos
        allowed = {'-id', 'id', '-anio', 'anio', '-precio', 'precio', 'nombre', '-nombre'}
        if order not in allowed:
            order = '-id'
        # opcional: random=1 para aleatorios
        if self.request.query_params.get('random') in {'1', 'true', 'True'}:
            return qs.order_by('?')
        return qs.order_by(order)

    @action(detail=False, methods=['get'], url_path='nacionales')
    def nacionales(self, request):
        base_country = request.query_params.get('base_country', 'Chile')
        vinos = self.get_queryset().filter(pais_origen__iexact=base_country)[:6]
        data = self.get_serializer(vinos, many=True).data
        return Response({"count": len(data), "results": data})

    @action(detail=False, methods=['get'], url_path='importados')
    def importados(self, request):
        base_country = request.query_params.get('base_country', 'Chile')
        vinos = self.get_queryset().exclude(pais_origen__iexact=base_country)[:6]
        data = self.get_serializer(vinos, many=True).data
        return Response({"count": len(data), "results": data})
    
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class VinoViewSet(viewsets.ModelViewSet):
    queryset = Vino.objects.all()
    serializer_class = VinoSerializer

    # --- NUEVO: endpoint público opcional ---
    @action(detail=False, methods=['get'], url_path='publicos', permission_classes=[AllowAny])
    def publicos(self, request):
        """Lista de vinos visible sin autenticación JWT"""
        queryset = self.get_queryset()[:6]  # puedes limitar los resultados
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
