from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0035_redsocial_tvdigital_radiodigital"),
    ]

    operations = [
        migrations.AddField(
            model_name="hechocriminal",
            name="creado_por",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name="hechos_criminales_creados",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

