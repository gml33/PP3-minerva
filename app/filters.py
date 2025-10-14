# app/filters.py

import django_filters

# Importamos solo los modelos principales que son clases de nivel superior.
# No importamos 'EstadoLink', 'EstadoArticulo', ni 'SituacionChoices' directamente aquí,
# ya que accedemos a sus 'choices' a través de los respectivos campos de los modelos.
from .models import (
    LinkRelevante,
    Actividad,
    Articulo,
    FichaIndividualizacion,
    TipoActividad,
    Categoria,
)


class LinkRelevanteFilter(django_filters.FilterSet):
    """
    Filtros para el modelo LinkRelevante.
    Permite filtrar por rangos de fechas, estado, diario digital y categorías.
    """

    fecha_carga_gte = django_filters.DateFilter(
        field_name="fecha_carga", lookup_expr="date__gte"
    )
    fecha_carga_lte = django_filters.DateFilter(
        field_name="fecha_carga", lookup_expr="date__lte"
    )

    estado = django_filters.ChoiceFilter(
        choices=LinkRelevante._meta.get_field("estado").choices
    )

    diario_digital = django_filters.CharFilter(
        field_name="diario_digital__nombre", lookup_expr="icontains"
    )
    categorias = django_filters.ModelMultipleChoiceFilter(
        field_name="categorias__id",
        queryset=Categoria.objects.all(),
        conjoined=False,  # Usa OR para múltiples selecciones
    )
    url_icontains = django_filters.CharFilter(
        field_name="url", lookup_expr="icontains", label="URL contiene"
    )

    class Meta:
        model = LinkRelevante
        fields = [
            "fecha_carga_gte",
            "fecha_carga_lte",
            "estado",
            "diario_digital",
            "categorias",
            "url_icontains",
        ]


class ActividadFilter(django_filters.FilterSet):
    """
    Filtros para el modelo Actividad.
    Permite filtrar por usuario, tipo de actividad y rango de fechas.
    """

    usuario = django_filters.CharFilter(
        field_name="usuario__username", lookup_expr="icontains", label="Usuario"
    )
    tipo = django_filters.ChoiceFilter(
        choices=TipoActividad.choices, label="Tipo de Actividad"
    )
    fecha_hora_gte = django_filters.DateTimeFilter(
        field_name="fecha_hora", lookup_expr="gte", label="Desde (Fecha y Hora)"
    )
    fecha_hora_lte = django_filters.DateTimeFilter(
        field_name="fecha_hora", lookup_expr="lte", label="Hasta (Fecha y Hora)"
    )
    descripcion_icontains = django_filters.CharFilter(
        field_name="descripcion", lookup_expr="icontains", label="Descripción contiene"
    )

    class Meta:
        model = Actividad
        fields = [
            "usuario",
            "tipo",
            "fecha_hora_gte",
            "fecha_hora_lte",
            "descripcion_icontains",
        ]


class ArticuloFilter(django_filters.FilterSet):
    """
    Filtros para el modelo Articulo.
    Permite filtrar por título, descripción, estado, fecha de generación y
    por campos relacionados de FichaIndividualizacion.
    """

    titulo__icontains = django_filters.CharFilter(
        field_name="titulo", lookup_expr="icontains", label="Título contiene"
    )
    descripcion__icontains = django_filters.CharFilter(
        field_name="descripcion", lookup_expr="icontains", label="Descripción contiene"
    )

    estado = django_filters.ChoiceFilter(
        choices=Articulo._meta.get_field("estado").choices, label="Estado del Artículo"
    )

    fecha_generacion__date__gte = django_filters.DateFilter(
        field_name="fecha_generacion__date",
        lookup_expr="gte",
        label="Fecha Generación Desde",
    )
    fecha_generacion__date__lte = django_filters.DateFilter(
        field_name="fecha_generacion__date",
        lookup_expr="lte",
        label="Fecha Generación Hasta",
    )

    # Filtros por campos de FichaIndividualizacion relacionada
    ficha_nombre_completo__icontains = django_filters.CharFilter(
        field_name="fichas_asociadas__nombre_completo",
        lookup_expr="icontains",
        label="Ficha - Nombre Completo",
    )
    ficha_dni__icontains = django_filters.CharFilter(
        field_name="fichas_asociadas__dni", lookup_expr="icontains", label="Ficha - DNI"
    )
    ficha_alias__icontains = django_filters.CharFilter(
        field_name="fichas_asociadas__alias",
        lookup_expr="icontains",
        label="Ficha - Alias",
    )
    # CAMBIO CRÍTICO AQUÍ: Accedemos a los choices de 'situacion' directamente del campo del modelo FichaIndividualizacion
    ficha_situacion = django_filters.ChoiceFilter(
        field_name="fichas_asociadas__situacion",
        choices=FichaIndividualizacion._meta.get_field("situacion").choices,
        label="Ficha - Situación",
    )

    class Meta:
        model = Articulo
        fields = [
            "titulo__icontains",
            "descripcion__icontains",
            "estado",
            "fecha_generacion__date__gte",
            "fecha_generacion__date__lte",
            "ficha_nombre_completo__icontains",
            "ficha_dni__icontains",
            "ficha_alias__icontains",
            "ficha_situacion",
        ]


class FichaIndividualizacionFilter(django_filters.FilterSet):
    """
    Filtros para el modelo FichaIndividualizacion.
    Permite filtrar por diversos campos de texto y opciones.
    """

    nombre_completo__icontains = django_filters.CharFilter(
        field_name="nombre_completo", lookup_expr="icontains", label="Nombre Completo"
    )
    dni__icontains = django_filters.CharFilter(
        field_name="dni", lookup_expr="icontains", label="DNI"
    )
    alias__icontains = django_filters.CharFilter(
        field_name="alias", lookup_expr="icontains", label="Alias"
    )
    banda__icontains = django_filters.CharFilter(
        field_name="banda", lookup_expr="icontains", label="Banda"
    )
    rol__icontains = django_filters.CharFilter(
        field_name="rol", lookup_expr="icontains", label="Rol"
    )
    nacionalidad__icontains = django_filters.CharFilter(
        field_name="nacionalidad", lookup_expr="icontains", label="Nacionalidad"
    )

    domicilio_linea1__icontains = django_filters.CharFilter(
        field_name="domicilio_linea1",
        lookup_expr="icontains",
        label="Domicilio Línea 1",
    )
    domicilio_linea2__icontains = django_filters.CharFilter(
        field_name="domicilio_linea2",
        lookup_expr="icontains",
        label="Domicilio Línea 2",
    )
    domicilio_linea3__icontains = django_filters.CharFilter(
        field_name="domicilio_linea3",
        lookup_expr="icontains",
        label="Domicilio Línea 3",
    )
    domicilio_linea4__icontains = django_filters.CharFilter(
        field_name="domicilio_linea4",
        lookup_expr="icontains",
        label="Domicilio Línea 4",
    )

    actividad__icontains = django_filters.CharFilter(
        field_name="actividad", lookup_expr="icontains", label="Actividad"
    )
    telefonos__icontains = django_filters.CharFilter(
        field_name="telefonos", lookup_expr="icontains", label="Teléfonos"
    )
    vehiculos__icontains = django_filters.CharFilter(
        field_name="vehiculos", lookup_expr="icontains", label="Vehículos"
    )

    # CAMBIO CRÍTICO AQUÍ: Accedemos a los choices de 'situacion' directamente del campo del modelo FichaIndividualizacion
    situacion = django_filters.ChoiceFilter(
        choices=FichaIndividualizacion._meta.get_field("situacion").choices,
        label="Situación",
    )

    fecha_creacion_gte = django_filters.DateFilter(
        field_name="fecha_creacion__date",
        lookup_expr="gte",
        label="Fecha Creación Desde",
    )
    fecha_creacion_lte = django_filters.DateFilter(
        field_name="fecha_creacion__date",
        lookup_expr="lte",
        label="Fecha Creación Hasta",
    )
    fecha_ultima_actualizacion_gte = django_filters.DateFilter(
        field_name="fecha_ultima_actualizacion__date",
        lookup_expr="gte",
        label="Fecha Última Actualización Desde",
    )
    fecha_ultima_actualizacion_lte = django_filters.DateFilter(
        field_name="fecha_ultima_actualizacion__date",
        lookup_expr="lte",
        label="Fecha Última Actualización Hasta",
    )

    articulos_relacionados__titulo__icontains = django_filters.CharFilter(
        field_name="articulos_relacionados__titulo",
        lookup_expr="icontains",
        label="Artículo Relacionado (Título)",
    )

    class Meta:
        model = FichaIndividualizacion
        fields = [
            "nombre_completo__icontains",
            "dni__icontains",
            "alias__icontains",
            "banda__icontains",
            "rol__icontains",
            "nacionalidad__icontains",
            "domicilio_linea1__icontains",
            "domicilio_linea2__icontains",
            "domicilio_linea3__icontains",
            "domicilio_linea4__icontains",
            "actividad__icontains",
            "telefonos__icontains",
            "vehiculos__icontains",
            "situacion",
            "fecha_creacion_gte",
            "fecha_creacion_lte",
            "fecha_ultima_actualizacion_gte",
            "fecha_ultima_actualizacion_lte",
            "articulos_relacionados__titulo__icontains",
        ]
