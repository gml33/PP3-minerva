from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0032_hechocriminal"),
    ]

    operations = [
        migrations.CreateModel(
            name="BandaCriminal",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=150, unique=True)),
                ("descripcion", models.TextField(blank=True)),
                (
                    "hechos",
                    models.ManyToManyField(
                        blank=True,
                        related_name="bandas_involucradas",
                        to="app.hechocriminal",
                    ),
                ),
                (
                    "integrantes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="bandas_criminales",
                        to="app.informeindividual",
                    ),
                ),
            ],
            options={
                "verbose_name": "Banda Criminal",
                "verbose_name_plural": "Bandas Criminales",
                "ordering": ["nombre"],
            },
        ),
    ]

