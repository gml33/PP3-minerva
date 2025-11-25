import json
import re

from django.db import migrations, models


def normalizar_a_json(apps, schema_editor):
    Banda = apps.get_model("app", "BandaCriminal")
    for banda in Banda.objects.all():
        valor = banda.nombres
        nombres = []
        if isinstance(valor, list):
            nombres = [n.strip() for n in valor if isinstance(n, str) and n.strip()]
        elif isinstance(valor, str):
            partes = re.split(r"[,;/\n]+", valor)
            nombres = [parte.strip() for parte in partes if parte and parte.strip()]
        if not nombres and valor:
            nombres = [str(valor).strip()]
        banda.nombres = json.dumps(nombres, ensure_ascii=False)
        banda.save(update_fields=["nombres"])


def revertir_a_texto(apps, schema_editor):
    Banda = apps.get_model("app", "BandaCriminal")
    for banda in Banda.objects.all():
        valor = banda.nombres
        if isinstance(valor, str):
            try:
                nombres = json.loads(valor)
            except json.JSONDecodeError:
                nombres = [valor]
        else:
            nombres = valor or []
        banda.nombres = ", ".join(nombres)
        banda.save(update_fields=["nombres"])


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0056_alter_bandacriminal_options_and_more"),
    ]

    operations = [
        migrations.RunPython(normalizar_a_json, revertir_a_texto),
        migrations.AlterField(
            model_name="bandacriminal",
            name="nombres",
            field=models.JSONField(
                db_column="nombre",
                default=list,
                help_text="Lista de nombres o alias asociados a la banda.",
            ),
        ),
    ]
