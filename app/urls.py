from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    UserViewSet,
    DiarioDigitalViewSet,
    CategoriaViewSet,
    LinkRelevanteViewSet,
    LinkRedSocialViewSet,
    LinkTvDigitalViewSet,
    ArticuloViewSet,
    RedSocialViewSet,
    TvDigitalViewSet,
    RadioDigitalViewSet,
    prensa_view,
    login_view,
    logout_view,
    clasificacion_view,
    redaccion_view,
    actividad_view,
    ActividadViewSet,
    exportar_actividades_excel,
    exportar_actividades_pdf,
    actividad_debug_view,
    registrar_clic_link,
    exportar_articulo_pdf,
    InformeIndividualViewSet,
    informes_view,
    estadisticas_view,
    exportar_estadisticas_pdf,
    estadisticas_api_view,
    editar_individuo_view,
    informes_crear_view,
    eliminar_informe_view,
    api_detalle_informe,
    consulta_informes_view,
    eliminar_diario,
    editar_diario,
    crear_diario,
    eliminar_categoria,
    editar_categoria,
    crear_categoria,
    configuraciones,
    exportar_informe_pdf,
    lista_links,
    api_links,
    hechos_delictivos_view,
    exportar_links_relevantes,
    solicitud_info_portal_view,
    solicitud_info_portal_detalle_view,
    solicitud_info_portal_eliminar_view,
    solicitud_info_portal_editar_view,
    solicitud_info_crear_view,
    solicitudes_info_list_view,
    solicitud_info_detalle_view,
    herramientas_osint_view,
    crear_herramienta_osint,
    editar_herramienta_osint,
    eliminar_herramienta_osint,
    osint_panel_view,
    exportar_fuentes_osint,
    crear_red_social,
    editar_red_social,
    eliminar_red_social,
    crear_tv_digital,
    editar_tv_digital,
    eliminar_tv_digital,
    crear_radio_digital,
    editar_radio_digital,
    eliminar_radio_digital,
    crear_hecho_delictivo,
    editar_hecho_delictivo,
    eliminar_hecho_delictivo,
    hecho_delictivo_detalle_view,
    exportar_hecho_delictivo_pdf,
    articulo_editar_view,
    # NUEVAS APIs PARA PANEL DE CLASIFICACIÓN
    api_links_list,
    api_diarios,
    api_categorias,
    api_link_detail,
)

router = DefaultRouter()
router.register(r"usuarios", UserViewSet, basename="usuario")
router.register(r"diarios", DiarioDigitalViewSet)
router.register(r"categorias", CategoriaViewSet)
router.register(r"links", LinkRelevanteViewSet, basename="link")
router.register(r"links_red_social", LinkRedSocialViewSet, basename="linkredsocial")
router.register(r"links_tv_digital", LinkTvDigitalViewSet, basename="linktvdigital")
router.register(r"articulos", ArticuloViewSet)
router.register(r"actividades", ActividadViewSet, basename="actividad")
router.register(r"informes", InformeIndividualViewSet, basename="informe")
router.register(r"users", UserViewSet)
router.register(r"redes", RedSocialViewSet, basename="redsocial")
router.register(r"tv", TvDigitalViewSet, basename="tvdigital")
router.register(r"radios", RadioDigitalViewSet, basename="radiodigital")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda request: redirect("login/")),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("prensa/", prensa_view, name="prensa"),
    path("redaccion/", redaccion_view, name="redaccion"),
    path(
        "solicitud/informacion/",
        solicitud_info_portal_view,
        name="solicitud_info_portal",
    ),
    path(
        "solicitud/informacion/<int:pk>/eliminar/",
        solicitud_info_portal_eliminar_view,
        name="solicitud_info_portal_eliminar",
    ),
    path(
        "solicitud/informacion/<int:pk>/editar/",
        solicitud_info_portal_editar_view,
        name="solicitud_info_portal_editar",
    ),
    path(
        "solicitud/informacion/<int:pk>/",
        solicitud_info_portal_detalle_view,
        name="solicitud_info_portal_detalle",
    ),
    path(
        "solicitudes/informacion/",
        solicitudes_info_list_view,
        name="solicitudes_info_list",
    ),
    path(
        "solicitudes/informacion/crear/",
        solicitud_info_crear_view,
        name="solicitud_info_crear",
    ),
    path(
        "solicitudes/informacion/<int:pk>/",
        solicitud_info_detalle_view,
        name="solicitud_info_detalle",
    ),
    path(
        "herramientas/osint/",
        herramientas_osint_view,
        name="herramientas_osint",
    ),
    path(
        "herramientas/osint/exportar/",
        exportar_fuentes_osint,
        name="exportar_fuentes_osint",
    ),
    path(
        "herramientas/osint/crear/",
        crear_herramienta_osint,
        name="crear_herramienta_osint",
    ),
    path(
        "herramientas/osint/<int:id>/editar/",
        editar_herramienta_osint,
        name="editar_herramienta_osint",
    ),
    path(
        "herramientas/osint/<int:id>/eliminar/",
        eliminar_herramienta_osint,
        name="eliminar_herramienta_osint",
    ),
    path("osint/", osint_panel_view, name="osint_panel"),
    path(
        "hechos/delictivos/",
        hechos_delictivos_view,
        name="hechos_delictivos",
    ),
    path(
        "hechos/delictivos/crear/",
        crear_hecho_delictivo,
        name="crear_hecho_delictivo",
    ),
    path(
        "hechos/delictivos/<int:id>/",
        hecho_delictivo_detalle_view,
        name="hecho_delictivo_detalle",
    ),
    path(
        "hechos/delictivos/<int:id>/editar/",
        editar_hecho_delictivo,
        name="editar_hecho_delictivo",
    ),
    path(
        "hechos/delictivos/<int:id>/eliminar/",
        eliminar_hecho_delictivo,
        name="eliminar_hecho_delictivo",
    ),
    path(
        "hechos/delictivos/<int:id>/exportar_pdf/",
        exportar_hecho_delictivo_pdf,
        name="exportar_hecho_delictivo_pdf",
    ),
    path(
        "links/exportar/",
        exportar_links_relevantes,
        name="exportar_links_relevantes",
    ),
    path("clasificacion/", clasificacion_view, name="clasificacion"),
    path("actividad/", actividad_view, name="actividad"),
    path("actividad_debug/", actividad_debug_view, name="actividad_debug"),
    path("api/token/", obtain_auth_token, name="api_token_auth"),
    path("api/", include(router.urls)),
    
    # ==================== NUEVAS APIs PARA PANEL DE CLASIFICACIÓN ====================
    path("api/links_list/", api_links_list, name="api_links_list"),
    path("api/diarios/", api_diarios, name="api_diarios"),
    path("api/categorias/", api_categorias, name="api_categorias"),
    path("api/links/<int:link_id>/", api_link_detail, name="api_link_detail"),
    # =================================================================================
    
    path("api/actividad/clic_link/", registrar_clic_link, name="registrar_clic_link"),
    path("api/links_list_old/", api_links, name="api_links"),  # Mantener por compatibilidad
    path("api/lista_links/", lista_links, name="lista_links"),
    path(
        "actividades/exportar_excel/",
        exportar_actividades_excel,
        name="exportar_actividades_excel",
    ),
    path(
        "actividades/exportar_pdf/",
        exportar_actividades_pdf,
        name="exportar_actividades_pdf",
    ),
    path(
        "api/articulos/<int:id>/exportar_pdf/",
        exportar_articulo_pdf,
        name="exportar_articulo_pdf",
    ),
    path(
        "articulos/<int:id>/editar/",
        articulo_editar_view,
        name="articulo_editar",
    ),
    path("captcha/", include("captcha.urls")),
    path("informes/", informes_view, name="informes"),
    path("informes/crear/", informes_crear_view, name="crear_informe"),  # ✅ NUEVA RUTA
    path("estadisticas/", estadisticas_view, name="estadisticas"),
    path(
        "estadisticas/exportar_pdf/",
        exportar_estadisticas_pdf,
        name="exportar_estadisticas_pdf",
    ),
    path("api/estadisticas/", estadisticas_api_view, name="estadisticas_api"),
    path("individuos/editar/<int:id>/", editar_individuo_view, name="editar_individuo"),
    path("individuos/nuevo/", editar_individuo_view, name="nuevo_individuo"),
    path(
        "individuos/eliminar/<int:id>/", eliminar_informe_view, name="eliminar_informe"
    ),
    path(
        "api/informes/<int:id>/detalle/",
        api_detalle_informe,
        name="api_detalle_informe",
    ),
    path("informes/<int:id>/eliminar/", eliminar_informe_view, name="eliminar_informe"),
    path("informes/editar/<int:id>/", editar_individuo_view, name="editar_individuo"),
    path("informes/consulta/", consulta_informes_view, name="consulta_informes"),
    path("configuraciones/", configuraciones, name="configuraciones"),
    # Categorías
    path("configuraciones/categoria/crear/", crear_categoria, name="crear_categoria"),
    path(
        "configuraciones/categoria/<int:id>/editar/",
        editar_categoria,
        name="editar_categoria",
    ),
    path(
        "configuraciones/categoria/<int:id>/eliminar/",
        eliminar_categoria,
        name="eliminar_categoria",
    ),
    # Diarios
    path("configuraciones/diario/crear/", crear_diario, name="crear_diario"),
    path(
        "configuraciones/diario/<int:id>/editar/", editar_diario, name="editar_diario"
    ),
    path(
        "configuraciones/diario/<int:id>/eliminar/",
        eliminar_diario,
        name="eliminar_diario",
    ),
    # Redes sociales
    path("configuraciones/red/crear/", crear_red_social, name="crear_red_social"),
    path(
        "configuraciones/red/<int:id>/editar/",
        editar_red_social,
        name="editar_red_social",
    ),
    path(
        "configuraciones/red/<int:id>/eliminar/",
        eliminar_red_social,
        name="eliminar_red_social",
    ),
    # TV Digital
    path("configuraciones/tv/crear/", crear_tv_digital, name="crear_tv_digital"),
    path(
        "configuraciones/tv/<int:id>/editar/",
        editar_tv_digital,
        name="editar_tv_digital",
    ),
    path(
        "configuraciones/tv/<int:id>/eliminar/",
        eliminar_tv_digital,
        name="eliminar_tv_digital",
    ),
    # Radio Digital
    path(
        "configuraciones/radio/crear/",
        crear_radio_digital,
        name="crear_radio_digital",
    ),
    path(
        "configuraciones/radio/<int:id>/editar/",
        editar_radio_digital,
        name="editar_radio_digital",
    ),
    path(
        "configuraciones/radio/<int:id>/eliminar/",
        eliminar_radio_digital,
        name="eliminar_radio_digital",
    ),
    path(
        "informes/<int:informe_id>/exportar/",
        exportar_informe_pdf,
        name="exportar_informe_pdf",
    ),
    path(
        "articulos/<int:id>/exportar_pdf/",
        exportar_articulo_pdf,
        name="exportar_articulo_pdf",
    ),
]
