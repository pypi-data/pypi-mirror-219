# Generated by Django 3.2.8 on 2022-04-19 18:36

import edc_model.models.fields.other_charfield
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_lists", "0008_delete_medicinesday14"),
        ("effect_subject", "0035_auto_20220414_1527"),
    ]

    operations = [
        migrations.AddField(
            model_name="chestxray",
            name="chest_xray_results_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalchestxray",
            name="chest_xray_results_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="chestxray",
            name="chest_xray_results",
            field=models.ManyToManyField(
                blank=True,
                to="effect_lists.XRayResults",
                verbose_name="If yes, what were the results?",
            ),
        ),
    ]
