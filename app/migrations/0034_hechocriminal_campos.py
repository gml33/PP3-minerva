from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0033_bandacriminal"),
    ]

    operations = [
        migrations.AddField(
            model_name="hechocriminal",
            name="ubicacion",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hechocriminal",
            name="calificacion",
            field=models.CharField(
                choices=[("robo", "Robo"), ("hurto", "Hurto"), ("homicidio", "Homicidio")],
                default="robo",
                max_length=20,
            ),
        ),
    ]

