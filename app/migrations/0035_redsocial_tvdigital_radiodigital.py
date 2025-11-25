from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0034_hechocriminal_campos"),
    ]

    operations = [
        migrations.CreateModel(
            name="RadioDigital",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100, unique=True)),
                ("url_principal", models.URLField()),
                ("logo", models.ImageField(blank=True, help_text="Carga el logo de la radio digital.", null=True, upload_to="radio_digital/")),
            ],
            options={
                "verbose_name": "Radio Digital",
                "verbose_name_plural": "Radios Digitales",
                "ordering": ["nombre"],
            },
        ),
        migrations.CreateModel(
            name="RedSocial",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100, unique=True)),
                ("url_principal", models.URLField()),
                ("logo", models.ImageField(blank=True, help_text="Carga el logo de la red social.", null=True, upload_to="redes_sociales/")),
            ],
            options={
                "verbose_name": "Red Social",
                "verbose_name_plural": "Redes Sociales",
                "ordering": ["nombre"],
            },
        ),
        migrations.CreateModel(
            name="TvDigital",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100, unique=True)),
                ("url_principal", models.URLField()),
                ("logo", models.ImageField(blank=True, help_text="Carga el logo del canal de TV digital.", null=True, upload_to="tv_digital/")),
            ],
            options={
                "verbose_name": "TV Digital",
                "verbose_name_plural": "TV Digital",
                "ordering": ["nombre"],
            },
        ),
    ]

