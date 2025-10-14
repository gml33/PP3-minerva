from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from app.models import (
    UserProfile,
    Roles,
    DiarioDigital,
    Categoria,
    LinkRelevante,
    Articulo,
)

# Crear usuarios
usuarios_data = [
    {"username": "admin", "email": "admin@example.com", "rol": Roles.ADMIN},
    {"username": "prensa1", "email": "prensa1@example.com", "rol": Roles.PRENSA},
    {
        "username": "clasificador1",
        "email": "clasif1@example.com",
        "rol": Roles.CLASIFICACION,
    },
    {"username": "redactor1", "email": "redactor1@example.com", "rol": Roles.REDACCION},
    {
        "username": "produccion1",
        "email": "produccion1@example.com",
        "rol": Roles.GERENTE_PRODUCCION,
    },
]

usuarios = []
for u in usuarios_data:
    user, created = User.objects.get_or_create(
        username=u["username"], defaults={"email": u["email"]}
    )
    if created:
        user.set_password("123456")
        user.save()
    UserProfile.objects.get_or_create(user=user, defaults={"rol": u["rol"]})
    usuarios.append(user)

# Crear DiarioDigital
diario, _ = DiarioDigital.objects.get_or_create(
    nombre="La Voz Urbana", url_principal="https://lavozurbana.com"
)

# Crear Categorías
categorias = {}
for nombre in ["individualizacion", "bandas criminales", "conflictividad barrial"]:
    cat, _ = Categoria.objects.get_or_create(nombre=nombre)
    categorias[nombre] = cat

# Crear Links Relevantes
links = []
for i in range(3):
    link, _ = LinkRelevante.objects.get_or_create(
        url=f"https://lavozurbana.com/noticia-{i}",
        defaults={
            "fecha_carga": timezone.now() - timedelta(days=i),
            "cargado_por": usuarios[1],
            "diario_digital": diario,
            "estado": "aprobado",
            "fecha_aprobacion": timezone.now() - timedelta(days=i - 1),
        },
    )
    link.categorias.set(
        [categorias["bandas criminales"], categorias["conflictividad barrial"]]
    )
    links.append(link)

# Crear Artículo
articulo, _ = Articulo.objects.get_or_create(
    titulo="Informe Semanal de Redacción",
    defaults={
        "descripcion": "Este artículo contiene un resumen de los eventos más relevantes.",
        "fecha_generacion": timezone.now(),
        "generado_por": usuarios[3],
    },
)
articulo.links_incluidos.set(links)

print("✅ Base de datos poblada con datos de ejemplo.")
