from django.db.utils import OperationalError, ProgrammingError

from .models import ConfiguracionSistema


def configuracion_sistema(request):
    sarcasmo = False
    try:
        sarcasmo = ConfiguracionSistema.obtener().sarcasmo_mode
    except (OperationalError, ProgrammingError):
        sarcasmo = False
    return {
        "sarcasmo_mode": sarcasmo,
    }
