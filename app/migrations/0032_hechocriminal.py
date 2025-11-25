from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0031_herramientaosint_tipo"),
    ]

    operations = [
        migrations.CreateModel(
            name="HechoCriminal",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha", models.DateField()),
                ("descripcion", models.TextField()),
                (
                    "autor",
                    models.ManyToManyField(
                        blank=True,
                        related_name="hechos_criminales_autor",
                        to="app.informeindividual",
                    ),
                ),
                (
                    "categoria",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.SET_NULL,
                        to="app.categoria",
                    ),
                ),
                (
                    "noticias",
                    models.ManyToManyField(
                        blank=True,
                        related_name="hechos_criminales",
                        to="app.linkrelevante",
                    ),
                ),
            ],
            options={
                "verbose_name": "Hecho Criminal",
                "verbose_name_plural": "Hechos Criminales",
                "ordering": ["-fecha"],
            },
        ),
    ]

