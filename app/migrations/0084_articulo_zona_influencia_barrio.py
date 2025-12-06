from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0083_rename_informes_role_to_editor"),
    ]

    operations = [
        migrations.AddField(
            model_name="articulo",
            name="zona_influencia",
            field=models.CharField(
                blank=True,
                max_length=255,
                help_text="Zona o territorio al que se asocia el artículo.",
            ),
        ),
        migrations.AddField(
            model_name="articulo",
            name="barrio",
            field=models.CharField(
                blank=True,
                max_length=150,
                help_text="Barrio específico relacionado al hecho redactado.",
            ),
        ),
    ]
