# Generated by Django 3.2.8 on 2022-05-10 13:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0059_auto_20220510_1544"),
        ("effect_lists", "0008_delete_medicinesday14"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BloodTests",
        ),
    ]
