from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0086_merge_0084_articulo_zone_editor"),
    ]

    operations = [
        migrations.AddField(
            model_name="articulo",
            name="localidad",
            field=models.CharField(
                blank=True,
                max_length=150,
                help_text="Localidad asociada al hecho redactado.",
            ),
        ),
        migrations.AddField(
            model_name="articulo",
            name="provincia",
            field=models.CharField(
                blank=True,
                max_length=150,
                help_text="Provincia relacionada al hecho redactado.",
            ),
        ),
    ]
