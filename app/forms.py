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
            "autor",
            "descripcion",
            "noticias",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "ubicacion": forms.TextInput(attrs={"class": "form-control"}),
            "calificacion": forms.Select(attrs={"class": "form-select"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["categoria"].required = False
        if user and not user.is_superuser:
            self.fields["autor"].queryset = InformeIndividual.objects.filter(
                generado_por=user
            )
            self.fields["noticias"].queryset = LinkRelevante.objects.filter(
                cargado_por=user
            )


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
