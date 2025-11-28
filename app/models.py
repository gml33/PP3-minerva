import json

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Roles definidos para los perfiles de usuario
class Roles(models.TextChoices):
    ADMIN = "administrador", "Administrador"
    PRENSA = "prensa", "Encargado de Prensa"
    CLASIFICACION = "clasificacion", "Encargado de Clasificación"
    REDACCION = "redaccion", "Encargado de Redacción"
    INFORMES = "informes", "Encargado de Informes"
    GERENCIA = "gerente", "Encargado de gerencia"
    GERENTE_PRODUCCION = "gerente_produccion", "Gerente de Producción"
    OBSERVADOR = "observador", "Observador"
    CLIENTE = "Cliente", "Cliente"


# Perfil extendido del usuario
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=Roles.choices)

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"


# Modelo DiarioDigital
class DiarioDigital(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    url_principal = models.URLField()
    # CAMPO DE IMAGEN PARA EL LOGO: Esto está correctamente definido
    logo = models.ImageField(
        upload_to="logos/",
        blank=True,
        null=True,
        help_text="Carga la imagen del logo del diario. Se recomienda un tamaño pequeño (ej. 30x30px).",
    )

    def __str__(self):
        return self.nombre

    # Propiedad para obtener la URL del logo: Esto también está correctamente definido
    @property
    def logo_url(self):
        if self.logo and hasattr(self.logo, "url"):
            # En un entorno de desarrollo, esto debería devolver la URL correcta.
            # En producción, asegúrate de que STATIC_URL y MEDIA_URL estén configurados correctamente.
            return self.logo.url
        return None


class RedSocial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    url_principal = models.URLField()
    logo = models.ImageField(
        upload_to="redes_sociales/",
        blank=True,
        null=True,
        help_text="Carga el logo de la red social.",
    )

    class Meta:
        verbose_name = "Red Social"
        verbose_name_plural = "Redes Sociales"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    @property
    def logo_url(self):
        if self.logo and hasattr(self.logo, "url"):
            return self.logo.url
        return None


class TvDigital(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    url_principal = models.URLField()
    logo = models.ImageField(
        upload_to="tv_digital/",
        blank=True,
        null=True,
        help_text="Carga el logo del canal de TV digital.",
    )

    class Meta:
        verbose_name = "TV Digital"
        verbose_name_plural = "TV Digital"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    @property
    def logo_url(self):
        if self.logo and hasattr(self.logo, "url"):
            return self.logo.url
        return None


class RadioDigital(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    url_principal = models.URLField()
    logo = models.ImageField(
        upload_to="radio_digital/",
        blank=True,
        null=True,
        help_text="Carga el logo de la radio digital.",
    )

    class Meta:
        verbose_name = "Radio Digital"
        verbose_name_plural = "Radios Digitales"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    @property
    def logo_url(self):
        if self.logo and hasattr(self.logo, "url"):
            return self.logo.url
        return None


class HerramientaOSINT(models.Model):
    class Tipo(models.TextChoices):
        GRATUITO = "gratuito", "Gratuito"
        PAGO = "pago", "Pago"

    nombre = models.CharField(max_length=150, unique=True)
    url = models.URLField()
    logo = models.ImageField(upload_to="herramientas_osint/", blank=True, null=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.GRATUITO,
    )

    class Meta:
        verbose_name = "Herramienta OSINT"
        verbose_name_plural = "Herramientas OSINT"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


# Modelo Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


# Estado posible para un link relevante
class EstadoLink(models.TextChoices):
    PENDIENTE = "pendiente", "Pendiente"
    APROBADO = "aprobado", "Aprobado"
    DESCARTADO = "descartado", "Descartado"


# Link relevante con categoría y estado
class LinkRelevante(models.Model):
    url = models.URLField(unique=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    cargado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="links_cargados"
    )
    # clasificado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="links_clasificados")
    diario_digital = models.ForeignKey(
        DiarioDigital, on_delete=models.SET_NULL, null=True, blank=True
    )
    estado = models.CharField(
        max_length=20, choices=EstadoLink.choices, default=EstadoLink.PENDIENTE
    )
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    categorias = models.ManyToManyField(Categoria, blank=True, related_name="links")
    revisado_clasificador = models.BooleanField(default=False)
    revisado_editor = models.BooleanField(default=False)
    revisado_redactor = models.BooleanField(default=False)
    clasificado_por_ia = models.BooleanField(default=False)
    confianza_clasificacion = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    resumen_ia = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Links Relevantes"
        ordering = ["-fecha_carga"]

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if self.estado == EstadoLink.APROBADO and not self.fecha_aprobacion:
            self.fecha_aprobacion = timezone.now()
        elif self.estado != EstadoLink.APROBADO and self.fecha_aprobacion:
            self.fecha_aprobacion = None
        super().save(*args, **kwargs)


class LinkRedSocial(models.Model):
    url = models.URLField(unique=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    cargado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="links_red_social_cargados"
    )
    red_social = models.ForeignKey(
        RedSocial, on_delete=models.SET_NULL, null=True, blank=True, related_name="links"
    )
    estado = models.CharField(
        max_length=20, choices=EstadoLink.choices, default=EstadoLink.PENDIENTE
    )
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    categorias = models.ManyToManyField(
        Categoria, blank=True, related_name="links_red_social"
    )
    revisado_clasificador = models.BooleanField(default=False)
    revisado_editor = models.BooleanField(default=False)
    revisado_redactor = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Link de Red Social"
        verbose_name_plural = "Links de Redes Sociales"
        ordering = ["-fecha_carga"]

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if self.estado == EstadoLink.APROBADO and not self.fecha_aprobacion:
            self.fecha_aprobacion = timezone.now()
        elif self.estado != EstadoLink.APROBADO and self.fecha_aprobacion:
            self.fecha_aprobacion = None
        super().save(*args, **kwargs)


class LinkTvDigital(models.Model):
    url = models.URLField(unique=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    cargado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="links_tv_digital_cargados"
    )
    tv_digital = models.ForeignKey(
        TvDigital, on_delete=models.SET_NULL, null=True, blank=True, related_name="links"
    )
    estado = models.CharField(
        max_length=20, choices=EstadoLink.choices, default=EstadoLink.PENDIENTE
    )
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    categorias = models.ManyToManyField(
        Categoria, blank=True, related_name="links_tv_digital"
    )
    revisado_clasificador = models.BooleanField(default=False)
    revisado_editor = models.BooleanField(default=False)
    revisado_redactor = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Link de TV Digital"
        verbose_name_plural = "Links de TV Digital"
        ordering = ["-fecha_carga"]

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if self.estado == EstadoLink.APROBADO and not self.fecha_aprobacion:
            self.fecha_aprobacion = timezone.now()
        elif self.estado != EstadoLink.APROBADO and self.fecha_aprobacion:
            self.fecha_aprobacion = None
        super().save(*args, **kwargs)


class LinkRadioDigital(models.Model):
    url = models.URLField(unique=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    cargado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="links_radio_digital_cargados"
    )
    radio_digital = models.ForeignKey(
        RadioDigital, on_delete=models.SET_NULL, null=True, blank=True, related_name="links"
    )
    estado = models.CharField(
        max_length=20, choices=EstadoLink.choices, default=EstadoLink.PENDIENTE
    )
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    categorias = models.ManyToManyField(
        Categoria, blank=True, related_name="links_radio_digital"
    )
    revisado_clasificador = models.BooleanField(default=False)
    revisado_editor = models.BooleanField(default=False)
    revisado_redactor = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Link de Radio Digital"
        verbose_name_plural = "Links de Radio Digital"
        ordering = ["-fecha_carga"]

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if self.estado == EstadoLink.APROBADO and not self.fecha_aprobacion:
            self.fecha_aprobacion = timezone.now()
        elif self.estado != EstadoLink.APROBADO and self.fecha_aprobacion:
            self.fecha_aprobacion = None
        super().save(*args, **kwargs)


class Domicilio(models.Model):
    calle = models.CharField(max_length=200, blank=True)
    altura = models.IntegerField(blank=True)
    barrio = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    provincia = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.calle} - {self.altura} - {self.barrio} - {self.ciudad} - {self.provincia}"


class Vehiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    dominio = models.CharField(max_length=20)
    color = models.CharField(max_length=50, blank=True, null=True)  # 👈 nuevo campo

    def __str__(self):
        return f"{self.marca} - {self.modelo} - {self.dominio} - {self.color}"


class Telefono(models.Model):
    numero = models.IntegerField()


class Empleador(models.Model):
    nombre = models.CharField(max_length=200)
    cuit = models.IntegerField(blank=True)
    fecha_alta = models.DateField()
    fecha_baja = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Razón social: {self.nombre} - CUIT: {self.cuit} - desde: {self.fecha_alta} - hasta: {self.fecha_baja}"


class Alias(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Vinculo(models.Model):
    nombre_apellido = models.CharField(max_length=200)
    dni = models.IntegerField(blank=True)
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre_apellido} - {self.dni} - {self.tipo}"


class HechoDestacado(models.Model):
    descripcion = models.TextField()
    lugar = models.CharField(max_length=200)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.fecha} - {self.lugar} - {self.descripcion}"


# Artículo generado con links incluidos
class Articulo(models.Model):
    class Estado(models.TextChoices):
        EN_REDACCION = "en redaccion", "En redacción"
        PENDIENTE_DE_INFORMACION = (
            "pendiente de informacion",
            "Pendiente de información",
        )
        COMPLETO = "completo", "Completo"

    titulo = models.CharField(max_length=200)
    fecha = models.DateField(null=True, blank=True)
    # ⚠️ CAMPO NUEVO AGREGADO: Fecha del Hecho
    fecha_hecho = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha del Hecho",
        help_text="Fecha en que ocurrió el hecho"
    )
    lugar = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField()
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    generado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="articulos_generados"
    )
    estado = models.CharField(
        max_length=30,
        choices=Estado.choices,
        default=Estado.EN_REDACCION,
    )
    fecha_modificacion = models.DateTimeField(auto_now=True)
    links_incluidos = models.ManyToManyField(LinkRelevante, related_name="articulos")
    hechos_destacados = models.ManyToManyField(HechoDestacado, blank=True)
    solicitudes_info = models.ManyToManyField(
        "SolicitudInfo", related_name="articulos"
    )
    revisado_redactor = models.BooleanField(default=False)
    fecha_generado_por_redaccion = models.DateTimeField(null=True, blank=True)
    fecha_leido_por_prensa = models.DateTimeField(null=True, blank=True)
    fecha_redactado_por_prensa = models.DateTimeField(null=True, blank=True)
    fecha_leido_por_redaccion = models.DateTimeField(null=True, blank=True)
    fecha_aprobado_por_redaccion = models.DateTimeField(null=True, blank=True)
    aprobacion = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Artículos"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.titulo


# Tipos de actividad para tracking
class TipoActividad(models.TextChoices):
    LOGIN = "login", "Inicio de sesión"
    LOGOUT = "logout", "Cierre de sesión"
    CARGA_LINK = "carga_link", "Carga de Link"
    CAMBIO_ESTADO = "cambio_estado", "Cambio de Estado"
    CLIC_LINK = "clic_link", "Clic en Link"
    CREACION_ARTICULO = "creacion_articulo", "Creación de Artículo"
    CLASIFICACION_LINK = "clasificacion_link", "Clasificacion del Link"
    CARGA_INFORME = "carge_informe", "carga de informe"
    OTRO = "otro", "Otro"
    EXPORTAR_INFORME_BANDA = "exportar_informe_banda", "Exportó informe de banda"


class SolicitudInfo(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_creador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="solicitudes_creadas",
    )
    descripcion = models.TextField()
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    respuesta = models.TextField(blank=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    respondido_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitudes_respondidas",
    )

    class Meta:
        verbose_name = "Solicitud de Información"
        verbose_name_plural = "Solicitudes de Información"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Solicitud #{self.pk} - {self.usuario_creador.username}"


# Registro de actividades de usuario
class Actividad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tipo = models.CharField(max_length=30, choices=TipoActividad.choices)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Actividades"
        ordering = ["-fecha_hora"]

    def __str__(self):
        return f"{self.usuario} - {self.get_tipo_display()} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"


# agregar una fecha por cada vez que se actualiza el informe, algo como un date_add_now_true.
class InformeIndividual(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = "masculino", "Masculino"
        FEMENINO = "femenino", "Femenino"

    apellido = models.CharField(max_length=100, blank=True)
    nombre = models.CharField(max_length=100, blank=True)
    documento = models.CharField(max_length=8, blank=True)
    cuit = models.IntegerField(blank=True, null=True)
    nacionalidad = models.CharField(max_length=50, blank=True)
    banda = models.CharField(max_length=100, blank=True)
    ROL_CHOICES = [
        ("soldadito", "Soldadito"),
        ("sicario", "Sicario"),
        ("lugarteniente", "Lugarteniente"),
        ("lider", "Lider"),
    ]
    SITUACION_CHOICES = [
        ("libertad", "Libertad"),
        ("fallecido", "Fallecido"),
        ("detenido", "Detenido"),
        ("domiciliaria", "Domiciliaria"),
        ("profugo", "Prófugo"),
    ]

    rol = models.CharField(max_length=20, choices=ROL_CHOICES, blank=True)
    situacion = models.CharField(max_length=20, choices=SITUACION_CHOICES, blank=True)
    sexo = models.CharField(
        max_length=20,
        choices=Sexo.choices,
        blank=True,
        help_text="Sexo registrado en el documento del individuo.",
    )
    actividad = models.CharField(max_length=200, blank=True)
    telefono = models.ManyToManyField(Telefono, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    domicilio = models.ManyToManyField(Domicilio, blank=True)
    vehiculos = models.ManyToManyField(Vehiculo, blank=True)
    empleadores = models.ManyToManyField(Empleador, blank=True)
    alias = models.ManyToManyField(Alias, blank=True)
    vinculos = models.ManyToManyField(Vinculo, blank=True)
    articulos = models.ManyToManyField(Articulo, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    generado_por = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="informes_generados",
    )
    foto = models.ImageField(
        upload_to="fotos_informes/",
        blank=True,
        null=True,
        help_text="Sube una foto relacionada con el informe.",
    )

    def __str__(self):
        return f"{self.apellido}, {self.nombre} - {self.documento}"


class HechoDelictivo(models.Model):
    class Calificacion(models.TextChoices):
        ROBO = "robo", "Robo"
        HURTO = "hurto", "Hurto"
        HOMICIDIO = "homicidio", "Homicidio"
        #agragr balaceras, etc

    class CategoriaTipo(models.TextChoices):
        ROBO = "robo", "Robo"
        HOMICIDIO = "homicidio", "Homicidio"
        DUELO_ESPADAS = "duelo_de_espadas", "Duelo de espadas"
        DESAMOR = "desamor", "Desamor"
        TRISTEZA = "tristeza", "Tristeza"
        VENTA_ORGANOS = "venta_de_organos", "Venta de organos"
        DUELO_BAILE = "duelo_de_baile", "Duelo de baile"


        #quitar categorias

    fecha = models.DateField()
    categoria = models.CharField(
        max_length=50,
        choices=CategoriaTipo.choices,
        null=True,
        blank=True,
    )
    ubicacion = models.JSONField(
        default=dict,
        blank=True,
        help_text="Detalle de ubicación con calle, número, barrio, localidad, ciudad y provincia.",
    )
    calificacion = models.CharField(
        max_length=20,
        choices=Calificacion.choices,
        default=Calificacion.ROBO,
    )
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hechos_criminales_creados",
    )
    autor = models.ManyToManyField(
        "InformeIndividual",
        related_name="hechos_criminales_autor",
        blank=True,
    )
    autor_desconocido = models.BooleanField(
        default=False,
        help_text="Marcá esta opción si no hay autores identificados.",
    )
    descripcion = models.TextField()
    noticias = models.ManyToManyField(
        "LinkRelevante",
        related_name="hechos_criminales",
        blank=True,
    )
    bandas = models.ManyToManyField(
        "BandaCriminal",
        related_name="hechos_delictivos",
        blank=True,
        help_text="Bandas criminales relacionadas con el hecho.",
    )
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.CASCADE,
        related_name="hechos_delictivos",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Hecho Delictivo"
        verbose_name_plural = "Hechos Delictivos"
        ordering = ["-fecha"]

    def __str__(self):
        categoria = self.get_categoria_display() if self.categoria else "Sin categoría"
        return f"{self.fecha} - {categoria}"

    def _ubicacion_dict(self):
        data = self.ubicacion or {}
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                data = {
                    "barrio": "",
                    "localidad": "",
                    "ciudad": data,
                    "provincia": "",
                }
        if not isinstance(data, dict):
            data = {}
        return {
            "calle": data.get("calle", ""),
            "numero": data.get("numero", ""),
            "barrio": data.get("barrio", ""),
            "localidad": data.get("localidad", ""),
            "ciudad": data.get("ciudad", ""),
            "provincia": data.get("provincia", ""),
        }

    @property
    def ubicacion_texto(self):
        data = self._ubicacion_dict()
        partes = []
        calle = data.get("calle", "").strip()
        numero = data.get("numero", "").strip()
        if calle and numero:
            partes.append(f"{calle} {numero}")
        elif calle:
            partes.append(calle)
        elif numero:
            partes.append(f"N° {numero}")
        partes.extend(
            [
                data.get("barrio", "").strip(),
                data.get("localidad", "").strip(),
                data.get("ciudad", "").strip(),
                data.get("provincia", "").strip(),
            ]
        )
        partes = [p for p in partes if p]
        return ", ".join(partes) if partes else "Ubicación no registrada"


class BandaCriminal(models.Model):
    nombres = models.JSONField(
        default=list,
        db_column="nombre",
        help_text="Lista de nombres o alias asociados a la banda.",
    )
    zonas_influencia = models.JSONField(
        default=list,
        blank=True,
        help_text="Listado de zonas con barrio, localidad, ciudad y provincia donde opera la banda.",
    )
    lideres = models.ManyToManyField(
        InformeIndividual,
        related_name="bandas_lideradas",
        blank=True,
    )
    miembros = models.ManyToManyField(
        InformeIndividual,
        related_name="bandas_miembro",
        blank=True,
    )
    bandas_aliadas = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="bandas_aliadas_de",
    )
    bandas_rivales = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="bandas_rivales_de",
    )
    class Meta:
        verbose_name = "Banda Criminal"
        verbose_name_plural = "Bandas Criminales"
        ordering = ["nombres"]

    def __str__(self):
        return self.nombre_principal or "Banda sin nombre"

    @property
    def nombre_principal(self):
        if isinstance(self.nombres, list) and self.nombres:
            return self.nombres[0]
        if isinstance(self.nombres, str):
            return self.nombres
        return ""

    @property
    def nombres_como_texto(self):
        if isinstance(self.nombres, list):
            return ", ".join(self.nombres)
        if isinstance(self.nombres, str):
            return self.nombres
        return ""

    def _zonas_influencia_list(self):
        data = self.zonas_influencia or []
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                data = []
        if not isinstance(data, list):
            return []
        zonas = []
        for zona in data:
            if isinstance(zona, dict):
                zonas.append(
                    {
                        "barrio": zona.get("barrio", "").strip(),
                        "localidad": zona.get("localidad", "").strip(),
                        "ciudad": zona.get("ciudad", "").strip(),
                        "provincia": zona.get("provincia", "").strip(),
                    }
                )
        return zonas

    @property
    def zonas_influencia_detalle(self):
        return self._zonas_influencia_list()

    @property
    def zonas_resumen(self):
        textos = []
        for zona in self._zonas_influencia_list():
            partes = [
                zona.get("barrio") or "",
                zona.get("localidad") or "",
                zona.get("ciudad") or "",
                zona.get("provincia") or "",
            ]
            texto = ", ".join([p for p in partes if p])
            if texto:
                textos.append(texto)
        return " / ".join(textos)


class InformeBandaCriminal(models.Model):
    banda = models.OneToOneField(
        BandaCriminal,
        on_delete=models.CASCADE,
        related_name="informes",
    )
    jerarquias_principales = models.ManyToManyField(
        "InformeIndividual",
        through="JerarquiaPrincipal",
        related_name="informes_banda_criminal",
        blank=True,
    )
    introduccion_descripcion = models.TextField(
        blank=True,
        help_text="Descripción de la introducción del informe.",
    )
    zonas_influencia = models.JSONField(
        default=list,
        blank=True,
        help_text="Listado estructurado de zonas donde opera la banda en el contexto del informe.",
    )
    conclusion_relevante = models.TextField(
        blank=True,
        help_text="Conclusión redactada por el redactor responsable.",
    )
    bandas_aliadas = models.ManyToManyField(
        BandaCriminal,
        related_name="informes_bandas_aliadas",
        symmetrical=False,
        blank=True,
    )
    bandas_rivales = models.ManyToManyField(
        BandaCriminal,
        related_name="informes_bandas_rivales",
        symmetrical=False,
        blank=True,
    )
    posible_evolucion = models.TextField(
        blank=True,
        help_text="Hipótesis u observaciones sobre la evolución de la banda.",
    )
    conclusiones_desarrollo = models.TextField(
        blank=True,
        help_text="Contenido del anexo de conclusiones.",
    )
    exportaciones = models.PositiveIntegerField(default=0)
    antecedentes = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de antecedentes personalizados que incluye título y descripción.",
    )
    desarrollo_titulo = models.CharField(
        max_length=255,
        blank=True,
        help_text="Título del apartado de desarrollo.",
    )
    desarrollo_contenido = models.TextField(
        blank=True,
        help_text="Contenido redactado manualmente para el desarrollo.",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Informe de Banda Criminal"
        verbose_name_plural = "Informes de Bandas Criminales"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"Informe de {self.banda.nombre_principal or 'Banda'}"

    def _zonas_influencia_list(self):
        data = self.zonas_influencia or []
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                data = []
        if not isinstance(data, list):
            return []
        zonas = []
        for zona in data:
            if isinstance(zona, dict):
                zonas.append(
                    {
                        "barrio": zona.get("barrio", "").strip(),
                        "localidad": zona.get("localidad", "").strip(),
                        "ciudad": zona.get("ciudad", "").strip(),
                        "provincia": zona.get("provincia", "").strip(),
                    }
                )
            elif isinstance(zona, str):
                zonas.append(
                    {
                        "barrio": "",
                        "localidad": "",
                        "ciudad": zona.strip(),
                        "provincia": "",
                    }
                )
        return zonas

    @property
    def zonas_influencia_detalle(self):
        return self._zonas_influencia_list()

    @property
    def zonas_resumen(self):
        textos = []
        for zona in self._zonas_influencia_list():
            partes = [
                zona.get("barrio") or "",
                zona.get("localidad") or "",
                zona.get("ciudad") or "",
                zona.get("provincia") or "",
            ]
            texto = ", ".join([p for p in partes if p])
            if texto:
                textos.append(texto)
        return " / ".join(textos)


class JerarquiaPrincipal(models.Model):
    class Rol(models.TextChoices):
        LIDER = "lider", "Líder"
        LUGARTENIENTE = "lugarteniente", "Lugarteniente"

    informe = models.ForeignKey(
        InformeBandaCriminal,
        on_delete=models.CASCADE,
        related_name="jerarquias",
    )
    miembro = models.ForeignKey(
        InformeIndividual,
        on_delete=models.CASCADE,
        related_name="jerarquias_de_banda",
    )
    rol = models.CharField(max_length=20, choices=Rol.choices)

    class Meta:
        verbose_name = "Jerarquía Principal"
        verbose_name_plural = "Jerarquías Principales"
        unique_together = ("informe", "miembro")

    def __str__(self):
        return f"{self.miembro} - {self.get_rol_display()} en {self.informe}"


class ConfiguracionSistema(models.Model):
    sarcasmo_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuración del Sistema"

    def __str__(self):
        return "Configuración del sistema"

    @classmethod
    def obtener(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"sarcasmo_mode": False})
        return obj
