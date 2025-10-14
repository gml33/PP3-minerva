from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0030_herramientaosint"),
    ]

    operations = [
        migrations.AddField(
            model_name="herramientaosint",
            name="tipo",
            field=models.CharField(
                choices=[("gratuito", "Gratuito"), ("pago", "Pago")],
                default="gratuito",
                max_length=20,
            ),
        ),
    ]

