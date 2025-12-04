import json

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField
from .models import (
    InformeIndividual,
    SolicitudInfo,
    Articulo,
    HerramientaOSINT,
    Categoria,
    DiarioDigital,
    RedSocial,
    TvDigital,
    RadioDigital,
    HechoDelictivo,
    BandaCriminal,
    LinkRelevante,
    LinkRedSocial,
    EstadoLink,
    InformeBandaCriminal,
    JerarquiaPrincipal,
    ConfiguracionSistema,
)


class CustomAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField(label="Verificación de Seguridad")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InformeIndividualForm(forms.ModelForm):
    class Meta:
        model = InformeIndividual
        fields = [
            "apellido",
            "nombre",
            "documento",
            "cuit",
            "nacionalidad",
            "sexo",
            "banda",
            "actividad",
            "fecha_nacimiento",
            "rol",
            "situacion",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rol"].required = False
        self.fields["situacion"].required = False

    def clean_documento(self):
        documento = (self.cleaned_data.get("documento") or "").strip()
        if not documento:
            return documento
        qs = InformeIndividual.objects.filter(documento=documento)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                "Ya existe un informe cargado con ese número de documento."
            )
        return documento

    def clean(self):
        cleaned_data = super().clean()
        banda = cleaned_data.get("banda")
        rol = (cleaned_data.get("rol") or "").strip()
        if banda and not rol:
            self.add_error(
                "rol",
                "Seleccioná el rol que ocupa en la banda asociada.",
            )
        return cleaned_data


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
        }


class DiarioForm(forms.ModelForm):
    class Meta:
        model = DiarioDigital
        fields = ["nombre", "url_principal", "logo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "url_principal": forms.URLInput(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class RedSocialForm(forms.ModelForm):
    class Meta:
        model = RedSocial
        fields = ["nombre", "url_principal", "logo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "url_principal": forms.URLInput(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class TvDigitalForm(forms.ModelForm):
    class Meta:
        model = TvDigital
        fields = ["nombre", "url_principal", "logo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "url_principal": forms.URLInput(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class RadioDigitalForm(forms.ModelForm):
    class Meta:
        model = RadioDigital
        fields = ["nombre", "url_principal", "logo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "url_principal": forms.URLInput(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class BandaCriminalForm(forms.ModelForm):
    links_diarios = forms.CharField(required=False, widget=forms.HiddenInput())
    links_redes = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = BandaCriminal
        fields = [
            "nombre",
            "alias",
            "zonas_influencia",
            "bandas_aliadas",
            "bandas_rivales",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "alias": forms.HiddenInput(),
            "zonas_influencia": forms.HiddenInput(),
            "bandas_aliadas": forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
            "bandas_rivales": forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
        }
        labels = {
            "nombre": "Nombre principal",
            "alias": "Alias",
            "zonas_influencia": "Zonas de influencia",
            "bandas_aliadas": "Bandas aliadas",
            "bandas_rivales": "Bandas rivales",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        def _label_banda(obj):
            return obj.nombres_como_texto or "Banda sin nombre"
        if not self.is_bound:
            alias = getattr(self.instance, "alias", []) or []
            if isinstance(alias, str):
                try:
                    alias = json.loads(alias)
                except json.JSONDecodeError:
                    alias = [alias] if alias else []
            self.fields["alias"].initial = json.dumps(alias or [], ensure_ascii=False)
            zonas = getattr(self.instance, "zonas_influencia", []) or []
            if isinstance(zonas, str):
                try:
                    zonas = json.loads(zonas)
                except json.JSONDecodeError:
                    zonas = []
            self.fields["zonas_influencia"].initial = json.dumps(zonas or [], ensure_ascii=False)
            self.fields["links_diarios"].initial = json.dumps(
                self._links_ids_from_instance("links_aprobados_diario"), ensure_ascii=False
            )
            self.fields["links_redes"].initial = json.dumps(
                self._links_ids_from_instance("links_aprobados_red_social"), ensure_ascii=False
            )
        bandas_queryset = BandaCriminal.objects.order_by("nombre")
        if self.instance and self.instance.pk:
            bandas_queryset = bandas_queryset.exclude(pk=self.instance.pk)
        for field_name in ("bandas_aliadas", "bandas_rivales"):
            self.fields[field_name].queryset = bandas_queryset
            self.fields[field_name].label_from_instance = _label_banda

    def _links_ids_from_instance(self, attr):
        if not self.instance or not self.instance.pk:
            return []
        manager = getattr(self.instance, attr, None)
        if not hasattr(manager, "values_list"):
            return []
        return list(manager.all().order_by("pk").values_list("id", flat=True))

    def clean_nombre(self):
        nombre = (self.cleaned_data.get("nombre") or "").strip()
        if not nombre:
            raise forms.ValidationError("Ingresá el nombre principal de la banda.")
        return nombre

    def clean_alias(self):
        raw = self.cleaned_data.get("alias")
        if isinstance(raw, list):
            alias = raw
        else:
            if not raw:
                alias = []
            else:
                try:
                    alias = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise forms.ValidationError(
                        "No se pudieron procesar los alias ingresados."
                    ) from exc
        alias_limpios = []
        for nombre in alias:
            if isinstance(nombre, str):
                valor = nombre.strip()
                if valor:
                    alias_limpios.append(valor)
        return alias_limpios

    def clean_zonas_influencia(self):
        raw = self.cleaned_data.get("zonas_influencia")
        if isinstance(raw, list):
            zonas = raw
        else:
            if not raw:
                zonas = []
            else:
                try:
                    zonas = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise forms.ValidationError(
                        "No se pudieron procesar las zonas de influencia."
                    ) from exc

        zonas_limpias = []
        for zona in zonas:
            if not isinstance(zona, dict):
                continue
            barrio = zona.get("barrio", "").strip()
            localidad = zona.get("localidad", "").strip()
            ciudad = zona.get("ciudad", "").strip()
            provincia = zona.get("provincia", "").strip()
            if any([barrio, localidad, ciudad, provincia]):
                zonas_limpias.append(
                    {
                        "barrio": barrio,
                        "localidad": localidad,
                        "ciudad": ciudad,
                        "provincia": provincia,
                    }
                )

        if not zonas_limpias:
            raise forms.ValidationError(
                "Ingresá al menos una zona de influencia con algún dato."
            )
        return zonas_limpias

    def _parse_ids_json(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return [int(v) for v in value if str(v).isdigit()]
        try:
            data = json.loads(value)
        except json.JSONDecodeError as exc:
            raise forms.ValidationError(
                "No se pudieron procesar los links asociados."
            ) from exc
        if not isinstance(data, list):
            raise forms.ValidationError("Formato inválido para los links seleccionados.")
        ids = []
        for entry in data:
            if isinstance(entry, int):
                ids.append(entry)
            elif isinstance(entry, str) and entry.isdigit():
                ids.append(int(entry))
        return ids

    def _categoria_bandas(self):
        if not hasattr(self, "_categoria_bandas_cache"):
            self._categoria_bandas_cache = Categoria.objects.filter(
                nombre__iexact="bandas criminales"
            ).first()
        return self._categoria_bandas_cache

    def clean_links_diarios(self):
        ids = self._parse_ids_json(self.cleaned_data.get("links_diarios"))
        if not ids:
            return []
        categoria = self._categoria_bandas()
        links = LinkRelevante.objects.filter(
            id__in=ids, estado=EstadoLink.APROBADO
        )
        if categoria:
            links = links.filter(categorias=categoria)
        links = list(links.distinct())
        return links

    def clean_links_redes(self):
        ids = self._parse_ids_json(self.cleaned_data.get("links_redes"))
        if not ids:
            return []
        categoria = self._categoria_bandas()
        links = LinkRedSocial.objects.filter(
            id__in=ids, estado=EstadoLink.APROBADO
        )
        if categoria:
            links = links.filter(categorias=categoria)
        links = list(links.distinct())
        return links

    def save(self, commit=True):
        banda = super().save(commit=commit)
        if commit:
            self._guardar_links_asociados(banda)
        else:
            self._guardar_links_en_m2m = True
        return banda

    def save_m2m(self):
        super().save_m2m()
        if getattr(self, "_guardar_links_en_m2m", False):
            self._guardar_links_asociados(self.instance)
            self._guardar_links_en_m2m = False

    def _guardar_links_asociados(self, banda):
        if not banda or not banda.pk:
            return
        banda.links_aprobados_diario.set(self.cleaned_data.get("links_diarios", []))
        banda.links_aprobados_red_social.set(self.cleaned_data.get("links_redes", []))


class InformeBandaCriminalForm(forms.ModelForm):
    antecedentes_json = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = InformeBandaCriminal
        fields = [
            "banda",
            "introduccion_descripcion",
            "conclusion_relevante",
            "posible_evolucion",
            "desarrollo_titulo",
            "desarrollo_contenido",
            "conclusiones_desarrollo",
        ]
        widgets = {
            "banda": forms.Select(attrs={"class": "form-select"}),
            "introduccion_descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "conclusion_relevante": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "posible_evolucion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "desarrollo_titulo": forms.TextInput(attrs={"class": "form-control"}),
            "desarrollo_contenido": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "conclusiones_desarrollo": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bandas_queryset = BandaCriminal.objects.order_by("nombre")
        self.fields["banda"].queryset = bandas_queryset
        self.fields["banda"].label_from_instance = (
            lambda obj: obj.nombres_como_texto or "Banda sin nombre"
        )
        self.fields["introduccion_descripcion"].required = False
        self.fields["conclusion_relevante"].required = False
        self.fields["posible_evolucion"].required = False
        self.fields["desarrollo_titulo"].required = False
        self.fields["desarrollo_contenido"].required = False
        self.fields["conclusiones_desarrollo"].required = False
        self.fields["desarrollo_titulo"].label = "Título"
        self.fields["desarrollo_contenido"].label = "Contenido"
        antecedentes_inicial = []
        if self.instance and getattr(self.instance, "antecedentes", None):
            antecedentes_inicial = self.instance.antecedentes
        self.fields["antecedentes_json"].initial = json.dumps(
            antecedentes_inicial or [], ensure_ascii=False
        )
        self._bandas_aliadas_auto = []
        self._bandas_rivales_auto = []
        self._lideres_auto = []
        self._lugartenientes_auto = []

    def _zonas_desde_banda(self, banda):
        zonas = getattr(banda, "zonas_influencia", []) or []
        if isinstance(zonas, str):
            try:
                zonas = json.loads(zonas)
            except json.JSONDecodeError:
                zonas = []
        if not isinstance(zonas, list):
            zonas = []
        return zonas

    def _lugartenientes_desde_banda(self, banda, lideres_ids):
        lug_por_rol = banda.miembros.filter(rol__iexact="lugarteniente").exclude(
            pk__in=lideres_ids
        )
        if lug_por_rol.exists():
            return list(lug_por_rol)
        integrantes = banda.miembros.exclude(pk__in=lideres_ids)
        return list(integrantes)

    def _aplicar_valores_por_defecto(self, banda):
        lideres_actual = list(banda.lideres.all())
        if not lideres_actual:
            lideres_actual = list(
                banda.miembros.filter(rol__iexact="lider")
            )
        lideres_ids = [miembro.pk for miembro in lideres_actual]
        lugartenientes_actual = self._lugartenientes_desde_banda(
            banda, lideres_ids
        )
        self._bandas_aliadas_auto = list(banda.bandas_aliadas.all())
        self._bandas_rivales_auto = list(banda.bandas_rivales.all())
        self._lideres_auto = lideres_actual
        self._lugartenientes_auto = lugartenientes_actual

    def save(self, commit=True):
        banda = self.cleaned_data.get("banda")
        if banda:
            self._aplicar_valores_por_defecto(banda)
        informe = super().save(commit=False)
        if banda:
            informe.zonas_influencia = self._zonas_desde_banda(banda)
        informe.antecedentes = self.cleaned_data.get("antecedentes", [])
        if commit:
            informe.save()
            self.save_m2m()
        return informe

    def _save_m2m(self):
        super()._save_m2m()
        informe = getattr(self, "instance", None)
        if informe and informe.pk:
            informe.bandas_aliadas.set(getattr(self, "_bandas_aliadas_auto", []))
            informe.bandas_rivales.set(getattr(self, "_bandas_rivales_auto", []))
            informe.jerarquias.all().delete()
            relaciones = []
            for miembro in getattr(self, "_lideres_auto", []):
                relaciones.append(
                    JerarquiaPrincipal(
                        informe=informe,
                        miembro=miembro,
                        rol=JerarquiaPrincipal.Rol.LIDER,
                    )
                )
            for miembro in getattr(self, "_lugartenientes_auto", []):
                relaciones.append(
                    JerarquiaPrincipal(
                        informe=informe,
                        miembro=miembro,
                        rol=JerarquiaPrincipal.Rol.LUGARTENIENTE,
                    )
                )
            if relaciones:
                JerarquiaPrincipal.objects.bulk_create(relaciones)


class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = [
            "titulo",
            "fecha",
            "lugar",
            "descripcion",
            "categoria",
            "estado",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "lugar": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 5}
            ),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].required = False


class HechoDelictivoForm(forms.ModelForm):
    ubicacion_calle = forms.CharField(
        required=False,
        label="Calle",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    ubicacion_numero = forms.CharField(
        required=False,
        label="Número",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    ubicacion_barrio = forms.CharField(
        required=False,
        label="Barrio",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    ubicacion_localidad = forms.CharField(
        required=False,
        label="Localidad",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    ubicacion_ciudad = forms.CharField(
        required=False,
        label="Ciudad",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    ubicacion_provincia = forms.CharField(
        required=False,
        label="Provincia",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    autor = forms.ModelMultipleChoiceField(
        queryset=InformeIndividual.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 8}),
        label="Autores",
    )
    autor_desconocido = forms.BooleanField(
        required=False,
        label="Autor no identificado",
        help_text="Tildá esta opción si todavía no tenés identificado al autor.",
    )
    noticias = forms.ModelMultipleChoiceField(
        queryset=LinkRelevante.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 8}),
        label="Noticias relacionadas",
    )
    bandas = forms.ModelMultipleChoiceField(
        queryset=BandaCriminal.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 8}),
        label="Bandas involucradas",
        help_text="Seleccioná las bandas relacionadas con el hecho, si corresponde.",
    )

    class Meta:
        model = HechoDelictivo
        fields = [
            "fecha",
            "categoria",
            "ubicacion",
            "calificacion",
            "articulo",
            "autor",
            "autor_desconocido",
            "descripcion",
            "noticias",
            "bandas",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "ubicacion": forms.HiddenInput(),
            "calificacion": forms.Select(attrs={"class": "form-select"}),
            "articulo": forms.Select(attrs={"class": "form-select"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["categoria"].required = False
        articulo_queryset = Articulo.objects.all().order_by("-fecha_creacion")
        links_queryset = LinkRelevante.objects.filter(
            estado=EstadoLink.APROBADO, revisado_clasificador=True
        ).order_by("-fecha_carga")

        autores_queryset = InformeIndividual.objects.all().order_by("apellido", "nombre")

        if user and not user.is_superuser:
            user_autores = autores_queryset.filter(generado_por=user)
            self.fields["autor"].queryset = (
                user_autores if user_autores.exists() else autores_queryset
            )

            articulo_queryset = articulo_queryset.filter(generado_por=user)

            user_links = links_queryset.filter(cargado_por=user)
            links_queryset = user_links if user_links.exists() else links_queryset
        else:
            self.fields["autor"].queryset = autores_queryset

        self.fields["noticias"].queryset = links_queryset
        bandas_queryset = BandaCriminal.objects.order_by("nombre")
        self.fields["bandas"].queryset = bandas_queryset
        self.fields["bandas"].label_from_instance = (
            lambda obj: obj.nombres_como_texto or "Banda sin nombre"
        )
        self.fields["articulo"].queryset = articulo_queryset
        self.fields["articulo"].required = True

        ubicacion_dict = self.instance._ubicacion_dict() if self.instance.pk else {}
        self.fields["ubicacion_calle"].initial = ubicacion_dict.get("calle", "")
        self.fields["ubicacion_numero"].initial = ubicacion_dict.get("numero", "")
        self.fields["ubicacion_barrio"].initial = ubicacion_dict.get("barrio", "")
        self.fields["ubicacion_localidad"].initial = ubicacion_dict.get("localidad", "")
        self.fields["ubicacion_ciudad"].initial = ubicacion_dict.get("ciudad", "")
        self.fields["ubicacion_provincia"].initial = ubicacion_dict.get("provincia", "")

    def clean(self):
        cleaned_data = super().clean()
        ubicacion = {
            "calle": cleaned_data.get("ubicacion_calle", "").strip(),
            "numero": cleaned_data.get("ubicacion_numero", "").strip(),
            "barrio": cleaned_data.get("ubicacion_barrio", "").strip(),
            "localidad": cleaned_data.get("ubicacion_localidad", "").strip(),
            "ciudad": cleaned_data.get("ubicacion_ciudad", "").strip(),
            "provincia": cleaned_data.get("ubicacion_provincia", "").strip(),
        }
        cleaned_data["ubicacion"] = ubicacion
        raw_antecedentes = cleaned_data.get("antecedentes_json") or "[]"
        try:
            data = json.loads(raw_antecedentes)
        except json.JSONDecodeError:
            raise forms.ValidationError(
                "No se pudo procesar la información de antecedentes. Intentá nuevamente."
            )
        antecedentes_limpios = []
        if isinstance(data, list):
            for item in data:
                titulo = (item.get("titulo") if isinstance(item, dict) else "").strip()
                descripcion = (
                    item.get("descripcion") if isinstance(item, dict) else ""
                ).strip()
                if titulo or descripcion:
                    antecedentes_limpios.append(
                        {"titulo": titulo, "descripcion": descripcion}
                    )
        cleaned_data["antecedentes"] = antecedentes_limpios
        return cleaned_data


class ConfiguracionSarcasmoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionSistema
        fields = ["sarcasmo_mode"]
        labels = {
            "sarcasmo_mode": "Activar Modo Sarcasmo",
        }


class SolicitudInfoForm(forms.ModelForm):
    articulos = forms.ModelMultipleChoiceField(
        queryset=Articulo.objects.none(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select",
                "size": 6,
            }
        ),
        label="Artículos relacionados",
    )

    class Meta:
        model = SolicitudInfo
        fields = ["descripcion"]
        widgets = {
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Detalle la información solicitada"}
            )
        }
        labels = {"descripcion": "Detalle de la solicitud"}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["articulos"].queryset = Articulo.objects.filter(
                generado_por=user
            ).order_by("-fecha_creacion")
        else:
            self.fields["articulos"].queryset = Articulo.objects.all().order_by(
                "-fecha_creacion"
            )
        self.fields["articulos"].label_from_instance = (
            lambda articulo: f"#{articulo.id} - {articulo.titulo or 'Sin título'}"
        )


class SolicitudInfoRespuestaForm(forms.ModelForm):
    class Meta:
        model = SolicitudInfo
        fields = ["respuesta", "documentacion"]
        widgets = {
            "respuesta": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Redactá la respuesta para el equipo de redacción"}
            ),
            "documentacion": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": ".pdf,.doc,.docx,.jpg,.jpeg,.png"}
            ),
        }
        labels = {
            "respuesta": "Respuesta",
            "documentacion": "Adjuntar documentación",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["respuesta"].required = True
        self.fields["documentacion"].required = False


class HerramientaOSINTForm(forms.ModelForm):
    class Meta:
        model = HerramientaOSINT
        fields = ["nombre", "url", "logo", "descripcion", "tipo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "nombre": "Nombre",
            "url": "URL",
            "logo": "Logo",
            "descripcion": "Descripción",
            "tipo": "Tipo",
        }
