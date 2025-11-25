from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0051_alter_userprofile_rol"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="HechoCriminal",
            new_name="HechoDelictivo",
        ),
        migrations.AlterModelOptions(
            name="hechodelictivo",
            options={
                "verbose_name": "Hecho Delictivo",
                "verbose_name_plural": "Hechos Delictivos",
                "ordering": ["-fecha"],
            },
        ),
    ]
