from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Registros
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponse
from.models import Manga
from .forms import MangaForm
from .models import MangaNuevo
from django.templatetags.static import static
from django.shortcuts import get_object_or_404

@csrf_exempt
def registro_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')

        # Verificar si el usuario ya existe
        if Registros.objects.filter(usuario=username).exists() or Registros.objects.filter(correo=email).exists():
            return JsonResponse({'error': 'El usuario no puede ser duplicado.','message':'usuario con parametros iguales.'})
        else:
            user = Registros()
            user.usuario = username
            user.correo = email
            user.contraseña = password
            user.save()

            return JsonResponse({'success': 'success', 'message': 'Registro exitoso'})
    else:    
          # Si la solicitud no es POST, devolver un mensaje JSON con error
        return JsonResponse({'status': 'error', 'message': 'Se esperaba una solicitud POST'})


@csrf_exempt
def logear_users(request):
    if request.method == 'POST':
        username = request.POST.get('username_r')
        password = request.POST.get('password_r')

        # Buscar el registro por el nombre de usuario
        registro = Registros.objects.filter(usuario=username,contraseña=password).first()
        user_id1=registro.id
        usuario=registro.usuario
        user_correo=registro.correo
        user_contra=registro.contraseña

        if registro:
            if registro.correo.endswith('@gmailVIP.com'):
                return JsonResponse({'redirect': 'http://localhost:9020/web/pagprincipalvip1/', 'user_id1': user_id1,'user_correo': user_correo,'usuario': usuario,'user_contra': user_contra})
            elif registro.correo.endswith('@gmail.com'):
                return JsonResponse({'redirect': 'http://localhost:9020/web/pagprincipalusuario/', 'user_id1': user_id1,'user_correo': user_correo,'usuario': usuario,'user_contra': user_contra})
            elif registro.correo.endswith('@gmailADMIN.com'):
                return JsonResponse({'redirect': 'http://localhost:9020/web/PagPrincipal/', 'user_id1': user_id1,'user_correo': user_correo,'usuario': usuario,'user_contra': user_contra})
            elif registro.correo.endswith('@gmailJEFE.com'):
                return JsonResponse({'redirect': 'http://localhost:9020/web/pagprincipalboss/', 'user_id1': user_id1,'user_correo': user_correo,'usuario': usuario,'user_contra': user_contra})
            else:
                return JsonResponse({'error': 'Correo electrónico inválido'})
        else:
            return JsonResponse({'error': 'Credenciales incorrectas','message':'Datos erroneos o nunca registrados'})

    else:
        return JsonResponse({'error': 'SOLO SOLICITUDES POST'})


@csrf_exempt
def registro_usuariow(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        contra = request.POST.get('contra')

        # Verificar si el usuario ya existe
        if Registros.objects.filter(usuario=username).exists() and Registros.objects.filter(correo=email).exists():
            return JsonResponse({'error': 'error papito', 'message': 'El usuario ya está registrado.'})
       
            
        else:
            user = Registros()
            user.usuario = username
            user.correo = email
            user.contraseña = contra
            user.save()

            return JsonResponse({'success': 'success papito', 'message': 'Registro exitoso'})

    # Si la solicitud no es POST, devolver un mensaje JSON con error
    return JsonResponse({'status': 'error', 'message': 'Se esperaba una solicitud POST'})


def cargar_usuarios(request):
    usuarios = Registros.objects.all()  # Obtener todos los usuarios de la base de datos
    usuarios_lista = [{'id': usuario.id, 'usuario': usuario.usuario, 'correo': usuario.correo  , 'contraseña':usuario.contraseña} for usuario in usuarios]
    return JsonResponse({'usuarios': usuarios_lista})



@csrf_exempt
def actualizar_usuario(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')
        new_username = request.POST.get('newUsername')
        new_email = request.POST.get('newEmail')
        new_password = request.POST.get('newPassword')

        try:
            user = Registros.objects.get(id=user_id)

            # Verificar si los nuevos datos son válidos y no están vacíos
            if new_username:
                # Verificar si el nuevo nombre de usuario no está vacío
                if not new_username.strip():
                    return JsonResponse({'status': 'error', 'message': 'El nombre de usuario no puede estar vacío'})
                user.usuario = new_username

            if new_email:
                # Verificar si el nuevo correo termina con '@gmail.com'
                if not (new_email.endswith('@gmail.com') or new_email.endswith('@gmailVIP.com') or new_email.endswith('@hotmail.com') or new_email.endswith('@hotmailVIP.com')):
                    return JsonResponse({'status': 'error', 'message': 'El correo electrónico debe terminar con "@gmail.com", "@gmailVIP.com", "@hotmail.com" o "@hotmailVIP.com"'})
                user.correo = new_email

            if new_password:
                user.contraseña = new_password

            user.save()
            return JsonResponse({'status': 'success', 'message': 'Usuario actualizado exitosamente'})
        except Registros.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'El usuario no existe'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Se esperaba una solicitud POST'})


@csrf_exempt
def eliminar_usuario(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')

        try:
            user = Registros.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'status': 'success', 'message': 'Usuario eliminado exitosamente'})
        except Registros.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'El usuario no existe'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Se esperaba una solicitud POST'})
    

@csrf_exempt
def verificar_vip(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contra = request.POST.get('contra')
        
        try:
            usuario= Registros.objects.get(contraseña=contra, correo=correo)
            if (usuario.correo.endswith('@gmailVIP.com') or usuario.correo.endswith('@hotmailVIP.com')):
                return JsonResponse({'success': True, 'message': 'El usuario es VIP'})
            else:
                return JsonResponse({'success': False, 'message': 'El usuario no es VIP'})
        except Registros.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Usuario no encontrado'})
    else:
        return JsonResponse({'error': 'SOLO SOLICITUDES POST'})

@csrf_exempt
def cargar_mangas(request):
    if request.method=='POST':
        manga_id=request.POST.get('id_manga')
        if MangaNuevo.objects.get(id=manga_id):
            manga = MangaNuevo.objects.get(id=manga_id)
            manga_data = {
                'id': manga.id,
                'nombre': manga.nombre,
                'precio': manga.precio
            }
            
            return JsonResponse({'success': 'Encontrado' ,'manga': manga_data})
    

@csrf_exempt
def create_manga(request):
    nombre = request.POST.get('nombre')
    precio = request.POST.get('precio')
    imagen = request.FILES.get('imagen')

    if nombre and precio and imagen:
        manga = MangaNuevo(nombre=nombre, precio=precio, imagen=imagen)
        manga.save()
        return JsonResponse({'message': 'Manga creado con éxito'}, status=201)
    else:
        return JsonResponse({'message': 'Faltan campos obligatorios'}, status=400)
    
   
@csrf_exempt
def eliminar_manga(request):
    if request.method == 'POST':
        id_manga = request.POST.get('idManga')
        manga = get_object_or_404(MangaNuevo, pk=id_manga)
        try:
            manga.delete()
            return JsonResponse({'success': True, 'message': 'Manga eliminado correctamente'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error al eliminar manga'})
    else:
        return JsonResponse({'success': False, 'message': 'Error: Solo solicitudes POST'})
    

@csrf_exempt
def obtener_mangas(request):
    if request.method == 'GET':
        mangas = MangaNuevo.objects.all().values('id', 'nombre', 'precio', 'imagen')
        mangas_list = [
            {
                'id': manga['id'],
                'nombre': manga['nombre'],
                'precio': manga['precio'],
                'imagen_url': static('mangas/' + manga['imagen'].split('/')[-1])
            } for manga in mangas
        ]
        return JsonResponse(mangas_list, safe=False)

