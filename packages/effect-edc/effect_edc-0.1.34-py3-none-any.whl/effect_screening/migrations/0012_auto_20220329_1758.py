# Generated by Django 3.2.11 on 2022-03-29 14:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("effect_screening", "0011_auto_20220329_1745"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalsubjectscreening",
            old_name="cm_on_csf",
            new_name="cm_in_csf",
        ),
        migrations.RenameField(
            model_name="historicalsubjectscreening",
            old_name="cm_on_csf_date",
            new_name="cm_in_csf_date",
        ),
        migrations.RenameField(
            model_name="historicalsubjectscreening",
            old_name="cm_on_csf_method",
            new_name="cm_in_csf_method",
        ),
        migrations.RenameField(
            model_name="historicalsubjectscreening",
            old_name="cm_on_csf_method_other",
            new_name="cm_in_csf_method_other",
        ),
        migrations.RenameField(
            model_name="subjectscreening",
            old_name="cm_on_csf",
            new_name="cm_in_csf",
        ),
        migrations.RenameField(
            model_name="subjectscreening",
            old_name="cm_on_csf_date",
            new_name="cm_in_csf_date",
        ),
        migrations.RenameField(
            model_name="subjectscreening",
            old_name="cm_on_csf_method",
            new_name="cm_in_csf_method",
        ),
        migrations.RenameField(
            model_name="subjectscreening",
            old_name="cm_on_csf_method_other",
            new_name="cm_in_csf_method_other",
        ),
    ]
