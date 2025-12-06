from django.db import migrations


def rename_informes_to_editor(apps, schema_editor):
    UserProfile = apps.get_model("app", "UserProfile")
    UserProfile.objects.filter(rol="informes").update(rol="editor")


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0082_bandacriminal_links_aprobados_diario_and_more"),
    ]

    operations = [
        migrations.RunPython(rename_informes_to_editor, migrations.RunPython.noop),
    ]
