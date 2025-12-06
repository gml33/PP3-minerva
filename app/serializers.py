from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Categoria,
    DiarioDigital,
    LinkRelevante,
    LinkRedSocial,
    LinkTvDigital,
    LinkRadioDigital,
    Articulo,
    InformeIndividual,
    Domicilio,
    Vehiculo,
    Empleador,
    Alias,
    Vinculo,
    HechoDestacado,
    Actividad,
    UserProfile,
    RedSocial,
    TvDigital,
    RadioDigital,
    SolicitudInfo,
)


# --------------------- SERIALIZADORES AUXILIARES ---------------------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "rol"]


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "userprofile"]


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre"]


class DiarioDigitalSerializer(serializers.ModelSerializer):
    logo_url = serializers.ReadOnlyField()

    class Meta:
        model = DiarioDigital
        fields = ["id", "nombre", "url_principal", "logo", "logo_url"]


class RedSocialSerializer(serializers.ModelSerializer):
    logo_url = serializers.ReadOnlyField()

    class Meta:
        model = RedSocial
        fields = ["id", "nombre", "url_principal", "logo", "logo_url"]


class TvDigitalSerializer(serializers.ModelSerializer):
    logo_url = serializers.ReadOnlyField()

    class Meta:
        model = TvDigital
        fields = ["id", "nombre", "url_principal", "logo", "logo_url"]


class RadioDigitalSerializer(serializers.ModelSerializer):
    logo_url = serializers.ReadOnlyField()

    class Meta:
        model = RadioDigital
        fields = ["id", "nombre", "url_principal", "logo", "logo_url"]


# ---------------------- LINK RELEVANTE ----------------------
class LinkRelevanteSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), many=True, write_only=True, required=False
    )
    categorias_info = serializers.SerializerMethodField(read_only=True)
    diario_logo_url = serializers.SerializerMethodField()
    diario_nombre = serializers.CharField(
        source="diario_digital.nombre", read_only=True
    )
    red_social = serializers.SerializerMethodField()
    red_social_nombre = serializers.SerializerMethodField()
    red_social_logo_url = serializers.SerializerMethodField()
    class Meta:
        model = LinkRelevante
        fields = [
            "id",
            "url",
            "fecha_carga",
            "cargado_por",
            "diario_digital",
            "diario_nombre",
            "diario_logo_url",
            "red_social",
            "red_social_nombre",
            "red_social_logo_url",
            "estado",
            "fecha_aprobacion",
            "categorias",
            "categorias_info",
            "revisado_clasificador",
            "revisado_editor",
            "revisado_redactor",
            "clasificado_por_ia",
            "confianza_clasificacion",
            "resumen_ia",
        ]
        read_only_fields = [
            "fecha_carga",
            "fecha_aprobacion",
            "cargado_por",
            "diario_nombre",
            "red_social_nombre",
        ]

    def get_diario_logo_url(self, obj):
        if obj.diario_digital and obj.diario_digital.logo:
            return obj.diario_digital.logo.url
        return None

    def get_red_social(self, obj):
        red = getattr(obj, "red_social", None)
        return red.id if red else None

    def get_red_social_nombre(self, obj):
        red = getattr(obj, "red_social", None)
        return red.nombre if red else None

    def get_red_social_logo_url(self, obj):
        red = getattr(obj, "red_social", None)
        if red and getattr(red, "logo", None):
            return red.logo.url
        return None

    def get_categorias_info(self, obj):
        return [{"id": cat.id, "nombre": cat.nombre} for cat in obj.categorias.all()]

    def update(self, instance, validated_data):
        categorias = validated_data.pop("categorias", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categorias is not None:
            instance.categorias.set(categorias)
        return instance


class LinkRedSocialSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), many=True, write_only=True, required=False
    )
    categorias_info = serializers.SerializerMethodField(read_only=True)
    red_social_nombre = serializers.CharField(
        source="red_social.nombre", read_only=True
    )
    red_social_logo_url = serializers.SerializerMethodField()

    class Meta:
        model = LinkRedSocial
        fields = [
            "id",
            "url",
            "fecha_carga",
            "cargado_por",
            "red_social",
            "red_social_nombre",
            "red_social_logo_url",
            "estado",
            "fecha_aprobacion",
            "categorias",
            "categorias_info",
            "revisado_clasificador",
            "revisado_editor",
            "revisado_redactor",
        ]
        read_only_fields = [
            "fecha_carga",
            "fecha_aprobacion",
            "cargado_por",
            "red_social_nombre",
        ]

    def get_red_social_logo_url(self, obj):
        red = obj.red_social
        if red and getattr(red, "logo", None):
            return red.logo.url
        return None

    def get_categorias_info(self, obj):
        return [{"id": cat.id, "nombre": cat.nombre} for cat in obj.categorias.all()]

    def update(self, instance, validated_data):
        categorias = validated_data.pop("categorias", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categorias is not None:
            instance.categorias.set(categorias)
        return instance


class LinkTvDigitalSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), many=True, write_only=True, required=False
    )
    categorias_info = serializers.SerializerMethodField(read_only=True)
    tv_digital_nombre = serializers.CharField(
        source="tv_digital.nombre", read_only=True
    )
    tv_digital_logo_url = serializers.SerializerMethodField()

    class Meta:
        model = LinkTvDigital
        fields = [
            "id",
            "url",
            "fecha_carga",
            "cargado_por",
            "tv_digital",
            "tv_digital_nombre",
            "tv_digital_logo_url",
            "estado",
            "fecha_aprobacion",
            "categorias",
            "categorias_info",
            "revisado_clasificador",
            "revisado_editor",
            "revisado_redactor",
        ]
        read_only_fields = [
            "fecha_carga",
            "fecha_aprobacion",
            "cargado_por",
            "tv_digital_nombre",
        ]

    def get_tv_digital_logo_url(self, obj):
        tv = obj.tv_digital
        if tv and getattr(tv, "logo", None):
            return tv.logo.url
        return None

    def get_categorias_info(self, obj):
        return [{"id": cat.id, "nombre": cat.nombre} for cat in obj.categorias.all()]

    def update(self, instance, validated_data):
        categorias = validated_data.pop("categorias", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categorias is not None:
            instance.categorias.set(categorias)
        return instance


class LinkRadioDigitalSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), many=True, write_only=True, required=False
    )
    categorias_info = serializers.SerializerMethodField(read_only=True)
    radio_digital_nombre = serializers.CharField(
        source="radio_digital.nombre", read_only=True
    )
    radio_digital_logo_url = serializers.SerializerMethodField()

    class Meta:
        model = LinkRadioDigital
        fields = [
            "id",
            "url",
            "fecha_carga",
            "cargado_por",
            "radio_digital",
            "radio_digital_nombre",
            "radio_digital_logo_url",
            "estado",
            "fecha_aprobacion",
            "categorias",
            "categorias_info",
            "revisado_clasificador",
            "revisado_editor",
            "revisado_redactor",
        ]
        read_only_fields = [
            "fecha_carga",
            "fecha_aprobacion",
            "cargado_por",
            "radio_digital_nombre",
        ]

    def get_radio_digital_logo_url(self, obj):
        radio = obj.radio_digital
        if radio and getattr(radio, "logo", None):
            return radio.logo.url
        return None

    def get_categorias_info(self, obj):
        return [{"id": cat.id, "nombre": cat.nombre} for cat in obj.categorias.all()]

    def update(self, instance, validated_data):
        categorias = validated_data.pop("categorias", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categorias is not None:
            instance.categorias.set(categorias)
        return instance


# ---------------------- HECHOS DESTACADOS ----------------------
class HechoDestacadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HechoDestacado
        fields = "__all__"


# ---------------------- MODELOS VARIOS ----------------------
class DomicilioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domicilio
        fields = "__all__"


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = "__all__"


class EmpleadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleador
        fields = "__all__"


class AliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias
        fields = "__all__"


class VinculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vinculo
        fields = "__all__"


# ---------------------- ARTICULO (CREATE / UPDATE) ----------------------
class ArticuloSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        allow_null=True,
        required=False,
    )
    links_incluidos = serializers.PrimaryKeyRelatedField(
        many=True, queryset=LinkRelevante.objects.all()
    )
    hechos_destacados = HechoDestacadoSerializer(
        many=True, required=False, allow_null=True
    )
    solicitudes_info = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SolicitudInfo.objects.all(),
        required=False,
    )
    generado_por = serializers.SerializerMethodField()

    class Meta:
        model = Articulo
        fields = [
            "id",
            "titulo",
            "fecha",  # Campo fecha original
            "fecha_hecho",  # ⚠️ NUEVO CAMPO AGREGADO
            "lugar",
            "descripcion",
            "categoria",
            "estado",
            "zona_influencia",
            "barrio",
            "localidad",
            "provincia",
            "fecha_creacion",
            "fecha_modificacion",
            "generado_por",
            "links_incluidos",
            "hechos_destacados",
            "revisado_redactor",
            "solicitudes_info",
        ]
        read_only_fields = ("generado_por",)

    def create(self, validated_data):
        hechos_data = validated_data.pop("hechos_destacados", [])
        links_data = validated_data.pop("links_incluidos", [])
        solicitudes_info_data = validated_data.pop("solicitudes_info", [])
        articulo = Articulo.objects.create(**validated_data)
        articulo.links_incluidos.set(links_data)
        if solicitudes_info_data:
            articulo.solicitudes_info.set(solicitudes_info_data)
        for hecho in hechos_data:
            articulo.hechos_destacados.add(HechoDestacado.objects.create(**hecho))
        return articulo

    def update(self, instance, validated_data):
        hechos_data = validated_data.pop("hechos_destacados", None)
        links_data = validated_data.pop("links_incluidos", None)
        solicitudes_info_data = validated_data.pop("solicitudes_info", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if links_data is not None:
            instance.links_incluidos.set(links_data)
        if hechos_data is not None:
            instance.hechos_destacados.clear()
            for hecho in hechos_data:
                instance.hechos_destacados.add(HechoDestacado.objects.create(**hecho))
        if solicitudes_info_data is not None:
            instance.solicitudes_info.set(solicitudes_info_data)
        return instance

    def get_generado_por(self, obj):
        if not obj.generado_por:
            return None
        return {
            "id": obj.generado_por.id,
            "username": obj.generado_por.username,
            "first_name": obj.generado_por.first_name,
            "last_name": obj.generado_por.last_name,
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        categoria = instance.categoria
        data["categoria"] = (
            {"id": categoria.id, "nombre": categoria.nombre}
            if categoria
            else None
        )

        data["links_incluidos"] = [
            {
                "id": link.id,
                "url": link.url,
                "fecha_carga": link.fecha_carga.isoformat()
                if link.fecha_carga
                else None,
                "diario_digital": link.diario_digital.nombre
                if link.diario_digital
                else None,
            }
            for link in instance.links_incluidos.all()
        ]

        data["solicitudes_info"] = [
            {
                "id": solicitud.id,
                "descripcion": solicitud.descripcion,
                "fecha_creacion": solicitud.fecha_creacion.isoformat()
                if solicitud.fecha_creacion
                else None,
            }
            for solicitud in instance.solicitudes_info.all()
        ]

        return data


# ---------- Articulo Detail ----------
class ArticuloDetailSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()
    links_incluidos = LinkRelevanteSerializer(many=True)
    hechos_destacados = HechoDestacadoSerializer(many=True)
    generado_por = serializers.SerializerMethodField()
    revisado_redactor = serializers.BooleanField()

    class Meta:
        model = Articulo
        fields = [
            "id",
            "titulo",
            "fecha",  # Campo fecha original
            "fecha_hecho",  # ⚠️ NUEVO CAMPO AGREGADO
            "descripcion",
            "categoria",
            "fecha_creacion",
            "fecha_modificacion",
            "generado_por",
            "links_incluidos",
            "hechos_destacados",
            "revisado_redactor",
        ]

    def get_generado_por(self, obj):
        return {
            "id": obj.generado_por.id,
            "username": obj.generado_por.username,
            "email": obj.generado_por.email,
        }


class InformeIndividualSerializer(serializers.ModelSerializer):
    domicilio = DomicilioSerializer(required=False, allow_null=True)
    foto = serializers.ImageField(required=False, allow_null=True)
    vehiculos = VehiculoSerializer(many=True, required=False, allow_null=True)
    empleadores = EmpleadorSerializer(many=True, required=False, allow_null=True)
    alias = AliasSerializer(many=True, required=False, allow_null=True)
    vinculos = VinculoSerializer(many=True, required=False, allow_null=True)
    articulos = serializers.PrimaryKeyRelatedField(
        queryset=Articulo.objects.all(), many=True, required=False, allow_null=True
    )

    class Meta:
        model = InformeIndividual
        fields = "__all__"

    def create(self, validated_data):
        domicilio_data = validated_data.pop("domicilio", None)
        vehiculos_data = validated_data.pop("vehiculos", [])
        empleadores_data = validated_data.pop("empleadores", [])
        alias_data = validated_data.pop("alias", [])
        vinculos_data = validated_data.pop("vinculos", [])
        articulos_data = validated_data.pop("articulos", [])

        domicilio = (
            Domicilio.objects.create(**domicilio_data) if domicilio_data else None
        )
        informe = InformeIndividual.objects.create(
            domicilio=domicilio, **validated_data
        )

        for veh in vehiculos_data or []:
            informe.vehiculos.add(Vehiculo.objects.create(**veh))
        for emp in empleadores_data or []:
            informe.empleadores.add(Empleador.objects.create(**emp))
        for al in alias_data or []:
            informe.alias.add(Alias.objects.create(**al))
        for vin in vinculos_data or []:
            informe.vinculos.add(Vinculo.objects.create(**vin))
        for art in articulos_data or []:
            informe.articulos.add(art)

        return informe

    def update(self, instance, validated_data):
        domicilio_data = validated_data.pop("domicilio", None)
        vehiculos_data = validated_data.pop("vehiculos", None)
        empleadores_data = validated_data.pop("empleadores", None)
        alias_data = validated_data.pop("alias", None)
        vinculos_data = validated_data.pop("vinculos", None)
        articulos_data = validated_data.pop("articulos", None)

        if domicilio_data:
            if instance.domicilio:
                for attr, value in domicilio_data.items():
                    setattr(instance.domicilio, attr, value)
                instance.domicilio.save()
            else:
                instance.domicilio = Domicilio.objects.create(**domicilio_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if vehiculos_data is not None:
            instance.vehiculos.clear()
            for veh in vehiculos_data:
                instance.vehiculos.add(Vehiculo.objects.create(**veh))

        if empleadores_data is not None:
            instance.empleadores.clear()
            for emp in empleadores_data:
                instance.empleadores.add(Empleador.objects.create(**emp))

        if alias_data is not None:
            instance.alias.clear()
            for al in alias_data:
                instance.alias.add(Alias.objects.create(**al))

        if vinculos_data is not None:
            instance.vinculos.clear()
            for vin in vinculos_data:
                instance.vinculos.add(Vinculo.objects.create(**vin))

        if articulos_data is not None:
            instance.articulos.set(articulos_data)

        return instance


# ---------------------- ACTIVIDAD ----------------------
class ActividadSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True
    )
    usuario_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Actividad
        fields = "__all__"
        read_only_fields = ["fecha_hora"]

    def get_usuario_nombre(self, obj):
        if obj.usuario:
            nombre = obj.usuario.get_full_name()
            return nombre.strip() if nombre and nombre.strip() else obj.usuario.username
        return None
