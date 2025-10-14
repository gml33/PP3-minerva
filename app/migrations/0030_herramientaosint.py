from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0029_solicitudinfo"),
    ]

    operations = [
        migrations.CreateModel(
            name="HerramientaOSINT",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=150, unique=True)),
                ("url", models.URLField()),
                ("logo", models.ImageField(blank=True, null=True, upload_to="herramientas_osint/")),
                ("descripcion", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Herramienta OSINT",
                "verbose_name_plural": "Herramientas OSINT",
                "ordering": ["nombre"],
            },
        ),
    ]

