import json

from django.db import migrations, models


def split_nombre_alias(apps, schema_editor):
    BandaCriminal = apps.get_model("app", "BandaCriminal")
    for banda in BandaCriminal.objects.all():
        valores = banda.nombres
        nombres_lista = []
        if isinstance(valores, list):
            nombres_lista = valores
        elif isinstance(valores, str) and valores:
            try:
                parsed = json.loads(valores)
            except json.JSONDecodeError:
                parsed = valores
            if isinstance(parsed, list):
                nombres_lista = parsed
            elif parsed:
                nombres_lista = [parsed]
        cleaned = [
            (valor or "").strip()
            for valor in nombres_lista
            if isinstance(valor, str) and valor.strip()
        ]
        if cleaned:
            nombre = cleaned[0]
            alias = cleaned[1:]
        else:
            nombre = banda.nombre or ""
            alias = []
        banda.nombre = nombre
        banda.alias = alias
        banda.save(update_fields=["nombre", "alias"])


def merge_nombre_alias(apps, schema_editor):
    BandaCriminal = apps.get_model("app", "BandaCriminal")
    for banda in BandaCriminal.objects.all():
        valores = []
        nombre = (banda.nombre or "").strip()
        if nombre:
            valores.append(nombre)
        alias = banda.alias or []
        if isinstance(alias, str):
            try:
                alias = json.loads(alias)
            except json.JSONDecodeError:
                alias = [alias] if alias else []
        if isinstance(alias, list):
            valores.extend(
                [a.strip() for a in alias if isinstance(a, str) and a.strip()]
            )
        banda.nombres = valores
        banda.save(update_fields=["nombres"])


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0079_alter_userprofile_rol"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bandacriminal",
            name="nombres",
            field=models.JSONField(
                db_column="nombres_json",
                default=list,
                help_text="Lista de nombres o alias asociados a la banda.",
            ),
        ),
        migrations.AddField(
            model_name="bandacriminal",
            name="nombre",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Nombre principal o denominación oficial de la banda.",
                max_length=255,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bandacriminal",
            name="alias",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="Lista de alias o denominaciones alternativas de la banda.",
            ),
        ),
        migrations.RunPython(split_nombre_alias, merge_nombre_alias),
        migrations.RemoveField(
            model_name="bandacriminal",
            name="nombres",
        ),
    ]
