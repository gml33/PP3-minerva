from django.apps import apps
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import (
    UserProfile,
    DiarioDigital,
    Categoria,
    LinkRelevante,
    LinkRedSocial,
    LinkTvDigital,
    Domicilio,
    Vehiculo,
    Telefono,
    Empleador,
    Alias,
    Vinculo,
    HechoDestacado,
    Articulo,
    Actividad,
    InformeIndividual,
    SolicitudInfo,
    HerramientaOSINT,
    HechoDelictivo,
    BandaCriminal,
    RedSocial,
    TvDigital,
    RadioDigital,
    LinkRadioDigital,
)

# Opcional: para personalizar visualización


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "rol")
    search_fields = ("user__username", "rol")


@admin.register(DiarioDigital)
class DiarioDigitalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "url_principal")
    search_fields = ("nombre",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(LinkRelevante)
class LinkRelevanteAdmin(ImportExportModelAdmin):
    list_display = ("url", "estado", "cargado_por", "fecha_carga")
    list_filter = ("estado", "fecha_carga", "cargado_por")
    search_fields = ("url", "cargado_por__username")

class LinkRelevanteResource(resources.ModelResource):
    class Meta:
        model = LinkRelevante
        fields = ("id", "url", "estado", "cargado_por", "fecha_carga")


@admin.register(LinkRedSocial)
class LinkRedSocialAdmin(ImportExportModelAdmin):
    list_display = ("url", "estado", "cargado_por", "fecha_carga")
    list_filter = ("estado", "fecha_carga", "cargado_por")
    search_fields = ("url", "cargado_por__username")


@admin.register(LinkTvDigital)
class LinkTvDigitalAdmin(ImportExportModelAdmin):
    list_display = ("url", "estado", "cargado_por", "fecha_carga")
    list_filter = ("estado", "fecha_carga", "cargado_por")
    search_fields = ("url", "cargado_por__username")


@admin.register(LinkRadioDigital)
class LinkRadioDigitalAdmin(ImportExportModelAdmin):
    list_display = ("url", "estado", "cargado_por", "fecha_carga")
    list_filter = ("estado", "fecha_carga", "cargado_por")
    search_fields = ("url", "cargado_por__username")


@admin.register(Articulo)
class ArticuloAdmin(ImportExportModelAdmin):
    list_display = ("titulo", "categoria", "generado_por", "fecha_creacion")
    list_filter = ("categoria", "fecha_creacion")
    search_fields = ("titulo", "descripcion", "generado_por__username")

class ArticuloResource(resources.ModelResource):
    class Meta:
        model = Articulo
        fields = ("id", "titulo", "categoria", "generado_por", "fecha_creacion")


@admin.register(InformeIndividual)
class InformeAdmin(ImportExportModelAdmin):
    list_display = ("apellido", "nombre", "documento", "generado_por", "fecha_creacion")
    search_fields = ("apellido", "nombre", "documento", "generado_por__username")

class InformeIndividualResource(resources.ModelResource):
    class Meta:
        model = InformeIndividual
        fields = ("id", "apellido", "nombre", "documento", "generado_por", "fecha_creacion")


@admin.register(Actividad)
class ActividadAdmin(ImportExportModelAdmin):
    list_display = ("usuario", "tipo", "fecha_hora")
    list_filter = ("tipo", "fecha_hora")
    search_fields = ("usuario__username", "descripcion")

class ActividadResource(resources.ModelResource):
    class Meta:
        model = Actividad
        fields = ("id", "usuario", "tipo", "fecha_hora", "descripcion")


@admin.register(SolicitudInfo)
class SolicitudInfoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario_creador",
        "fecha_creacion",
        "fecha_lectura",
        "fecha_respuesta",
        "respondido_por",
        "delete_button",
    )
    list_filter = ("fecha_creacion", "fecha_respuesta")
    search_fields = ("usuario_creador__username", "descripcion")

    def delete_button(self, obj):
        delete_url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete", args=[obj.pk]
        )
        return format_html(
            '<a class="button" style="color:#ba2121;" href="{}">Eliminar</a>', delete_url
        )

    delete_button.short_description = "Eliminar"


@admin.register(HerramientaOSINT)
class HerramientaOSINTAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "url")
    list_filter = ("tipo",)
    search_fields = ("nombre", "descripcion")


@admin.register(HechoDelictivo)
class HechoDelictivoAdmin(admin.ModelAdmin):
    list_display = ("fecha", "categoria", "ubicacion", "calificacion", "articulo", "creado_por")
    list_filter = ("fecha", "categoria", "calificacion")
    search_fields = ("descripcion", "ubicacion")
    filter_horizontal = ("autor", "noticias")


@admin.register(BandaCriminal)
class BandaCriminalAdmin(admin.ModelAdmin):
    list_display = ("nombres", "territorio_operacion", "cantidad_lideres", "cantidad_miembros")
    search_fields = ("nombres", "territorio_operacion")
    filter_horizontal = ("lideres", "miembros")

    @admin.display(description="Líderes")
    def cantidad_lideres(self, obj):
        return obj.lideres.count()

    @admin.display(description="Miembros")
    def cantidad_miembros(self, obj):
        return obj.miembros.count()


@admin.register(RedSocial)
class RedSocialAdmin(admin.ModelAdmin):
    list_display = ("nombre", "url_principal")
    search_fields = ("nombre",)


@admin.register(TvDigital)
class TvDigitalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "url_principal")
    search_fields = ("nombre",)


@admin.register(RadioDigital)
class RadioDigitalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "url_principal")
    search_fields = ("nombre",)


# El resto sin personalización
admin.site.register(Domicilio)
admin.site.register(Vehiculo)
admin.site.register(Telefono)
admin.site.register(Empleador)
admin.site.register(Alias)
admin.site.register(Vinculo)
admin.site.register(HechoDestacado)

# Register any remaining models so they appear in the admin automatically.
app_config = apps.get_app_config("app")
for model in app_config.get_models():
    if model not in admin.site._registry:
        admin.site.register(model)
