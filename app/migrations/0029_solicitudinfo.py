from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0028_alter_informeindividual_rol_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SolicitudInfo",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                ("descripcion", models.TextField()),
                ("fecha_lectura", models.DateTimeField(blank=True, null=True)),
                ("respuesta", models.TextField(blank=True)),
                ("fecha_respuesta", models.DateTimeField(blank=True, null=True)),
                (
                    "respondido_por",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.SET_NULL,
                        related_name="solicitudes_respondidas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "usuario_creador",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="solicitudes_creadas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Solicitud de Información",
                "verbose_name_plural": "Solicitudes de Información",
                "ordering": ["-fecha_creacion"],
            },
        ),
    ]

