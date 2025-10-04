from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Vino, Categoria

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

def registro(request):
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

