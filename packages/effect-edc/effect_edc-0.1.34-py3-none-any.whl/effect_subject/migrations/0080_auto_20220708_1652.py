# Generated by Django 3.2.13 on 2022-07-08 14:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0079_auto_20220704_1348"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalmedicationadherence",
            name="pill_count_not_performed_reason",
            field=models.TextField(
                blank=True, null=True, verbose_name="If NO, please specify reason ..."
            ),
        ),
        migrations.AddField(
            model_name="medicationadherence",
            name="pill_count_not_performed_reason",
            field=models.TextField(
                blank=True, null=True, verbose_name="If NO, please specify reason ..."
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="on_tb_tx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                verbose_name="Is the participant currently taking TB treatment?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="on_tb_tx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                verbose_name="Is the participant currently taking TB treatment?",
            ),
        ),
    ]
