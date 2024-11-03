# Generated by Django 5.0.1 on 2024-10-27 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("code_api", "0003_alter_codedocument_code"),
        ("contributors", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="codedocument",
            name="contributors",
            field=models.ManyToManyField(
                related_name="code_documents", to="contributors.contributor"
            ),
        ),
    ]
