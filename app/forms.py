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
    LinkRelevante,
    EstadoLink,
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
