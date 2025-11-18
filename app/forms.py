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
    EstadoLink,
    InformeBandaCriminal,
    JerarquiaPrincipal,
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
    class Meta:
        model = BandaCriminal
        fields = [
            "nombres",
            "zonas_influencia",
            "lideres",
            "miembros",
            "bandas_aliadas",
            "bandas_rivales",
        ]
        widgets = {
            "nombres": forms.HiddenInput(),
            "zonas_influencia": forms.HiddenInput(),
            "bandas_aliadas": forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
            "bandas_rivales": forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
        }
        labels = {
            "nombres": "Nombres o alias",
            "zonas_influencia": "Zonas de influencia",
            "bandas_aliadas": "Bandas aliadas",
            "bandas_rivales": "Bandas rivales",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            valores = self.instance.nombres if getattr(self.instance, "nombres", None) else []
            if isinstance(valores, str):
                try:
                    valores = json.loads(valores)
                except json.JSONDecodeError:
                    valores = [valores] if valores else []
            self.fields["nombres"].initial = json.dumps(valores or [], ensure_ascii=False)
            zonas = getattr(self.instance, "zonas_influencia", []) or []
            if isinstance(zonas, str):
                try:
                    zonas = json.loads(zonas)
                except json.JSONDecodeError:
                    zonas = []
            self.fields["zonas_influencia"].initial = json.dumps(zonas or [], ensure_ascii=False)

    def clean_nombres(self):
        raw = self.cleaned_data.get("nombres")
        if isinstance(raw, list):
            nombres = raw
        else:
            if not raw:
                nombres = []
            else:
                try:
                    nombres = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise forms.ValidationError(
                        "No se pudieron procesar los nombres ingresados."
                    ) from exc
        nombres_limpios = []
        for nombre in nombres:
            if isinstance(nombre, str):
                valor = nombre.strip()
                if valor:
                    nombres_limpios.append(valor)
        if not nombres_limpios:
            raise forms.ValidationError("Ingresá al menos un nombre para la banda.")
        return nombres_limpios

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


class InformeBandaCriminalForm(forms.ModelForm):
    lideres = forms.ModelMultipleChoiceField(
        queryset=InformeIndividual.objects.order_by("apellido", "nombre"),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
        label="Líderes",
        help_text="Seleccioná los miembros que actúan como líderes.",
    )
    lugartenientes = forms.ModelMultipleChoiceField(
        queryset=InformeIndividual.objects.order_by("apellido", "nombre"),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
        label="Lugartenientes",
        help_text="Seleccioná los miembros que actúan como lugartenientes.",
    )

    class Meta:
        model = InformeBandaCriminal
        fields = [
            "banda",
            "resumen_ejecutivo",
            "conclusion_relevante",
            "bandas_aliadas",
            "bandas_rivales",
            "posible_evolucion",
        ]
        widgets = {
            "banda": forms.Select(attrs={"class": "form-select"}),
            "resumen_ejecutivo": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "conclusion_relevante": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "bandas_aliadas": forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
            "bandas_rivales": forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
            "posible_evolucion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        labels = {
            "bandas_aliadas": "Bandas aliadas (opcional)",
            "bandas_rivales": "Bandas rivales (opcional)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["bandas_aliadas"].queryset = BandaCriminal.objects.order_by("nombres")
        self.fields["bandas_rivales"].queryset = BandaCriminal.objects.order_by("nombres")
        self.fields["bandas_aliadas"].required = False
        self.fields["bandas_rivales"].required = False
        self.fields["resumen_ejecutivo"].required = False
        self.fields["conclusion_relevante"].required = False
        self.fields["posible_evolucion"].required = False
        if self.instance and self.instance.pk:
            lideres_inicial = self.instance.jerarquias.filter(
                rol=JerarquiaPrincipal.Rol.LIDER
            ).values_list("miembro_id", flat=True)
            lugartenientes_inicial = self.instance.jerarquias.filter(
                rol=JerarquiaPrincipal.Rol.LUGARTENIENTE
            ).values_list("miembro_id", flat=True)
            self.fields["lideres"].initial = list(lideres_inicial)
            self.fields["lugartenientes"].initial = list(lugartenientes_inicial)

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

    def save(self, commit=True):
        informe = super().save(commit=False)
        informe.zonas_influencia = self._zonas_desde_banda(informe.banda)
        if commit:
            informe.save()
            self.save_m2m()
        return informe

    def save_m2m(self):
        super().save_m2m()
        informe = getattr(self, "instance", None)
        if informe and informe.pk:
            informe.jerarquias.all().delete()
            relaciones = []
            for miembro in self.cleaned_data.get("lideres", []):
                relaciones.append(
                    JerarquiaPrincipal(
                        informe=informe,
                        miembro=miembro,
                        rol=JerarquiaPrincipal.Rol.LIDER,
                    )
                )
            for miembro in self.cleaned_data.get("lugartenientes", []):
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
    autor = forms.ModelMultipleChoiceField(
        queryset=InformeIndividual.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 8}),
        label="Autores",
    )
    noticias = forms.ModelMultipleChoiceField(
        queryset=LinkRelevante.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 8}),
        label="Noticias relacionadas",
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
            "descripcion",
            "noticias",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "ubicacion": forms.TextInput(attrs={"class": "form-control"}),
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
        self.fields["articulo"].queryset = articulo_queryset
        self.fields["articulo"].required = True


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
        fields = ["respuesta"]
        widgets = {
            "respuesta": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Redactá la respuesta para el equipo de redacción"}
            )
        }
        labels = {"respuesta": "Respuesta"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["respuesta"].required = True


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
