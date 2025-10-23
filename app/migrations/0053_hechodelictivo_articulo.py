from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0052_rename_hechocriminal_to_hechodelictivo"),
    ]

    operations = [
        migrations.AddField(
            model_name="hechodelictivo",
            name="articulo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hechos_delictivos",
                to="app.articulo",
            ),
        ),
    ]
