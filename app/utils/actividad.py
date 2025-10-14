from ..models import Actividad


def log_actividad(request, tipo, descripcion):
    usuario = request.user if request.user.is_authenticated else None
    Actividad.objects.create(usuario=usuario, tipo=tipo, descripcion=descripcion)
