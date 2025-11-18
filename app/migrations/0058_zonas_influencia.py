import json

from django.db import migrations, models


def copiar_territorios_a_zonas(apps, schema_editor):
    Banda = apps.get_model("app", "BandaCriminal")
    for banda in Banda.objects.all():
        valor = getattr(banda, "territorio_operacion", "")
        zonas = []
        if valor:
            zonas.append(
                {
                    "barrio": "",
                    "localidad": "",
                    "ciudad": valor,
                    "provincia": "",
                }
            )
        banda.zonas_influencia = zonas
        banda.save(update_fields=["zonas_influencia"])


def restaurar_territorios(apps, schema_editor):
    Banda = apps.get_model("app", "BandaCriminal")
    for banda in Banda.objects.all():
        valor = banda.zonas_influencia or []
        if isinstance(valor, str):
            try:
                valor = json.loads(valor)
            except json.JSONDecodeError:
                valor = []
        textos = []
        for zona in valor or []:
            if not isinstance(zona, dict):
                continue
            partes = [
                zona.get("barrio", "").strip(),
                zona.get("localidad", "").strip(),
                zona.get("ciudad", "").strip(),
                zona.get("provincia", "").strip(),
            ]
            texto = ", ".join([p for p in partes if p])
            if texto:
                textos.append(texto)
        banda.territorio_operacion = " / ".join(textos)
        banda.save(update_fields=["territorio_operacion"])


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0057_alter_bandacriminal_nombres"),
    ]

    operations = [
        migrations.AddField(
            model_name="bandacriminal",
            name="zonas_influencia",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="Listado de zonas con barrio, localidad, ciudad y provincia donde opera la banda.",
            ),
        ),
        migrations.RunPython(copiar_territorios_a_zonas, restaurar_territorios),
        migrations.RemoveField(
            model_name="bandacriminal",
            name="territorio_operacion",
        ),
    ]
