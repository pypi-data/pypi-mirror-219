# Generated by Django 3.2.8 on 2022-03-09 12:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_ae", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aeinitial",
            name="date_admitted",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name='If "Yes", please specify date of hospital admission:',
            ),
        ),
        migrations.AddField(
            model_name="aeinitial",
            name="date_discharged",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name='If "Discharged", please specify date discharged:',
            ),
        ),
        migrations.AddField(
            model_name="aeinitial",
            name="fluconazole_relation",
            field=models.CharField(
                choices=[
                    ("not_related", "Not related"),
                    ("unlikely_related", "Unlikely related"),
                    ("possibly_related", "Possibly related"),
                    ("probably_related", "Probably related"),
                    ("definitely_related", "Definitely related"),
                    ("N/A", "Not applicable"),
                ],
                default="-",
                max_length=25,
                verbose_name="Relationship to study drugs: Fluconazole:",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="aeinitial",
            name="flucytosine_relation",
            field=models.CharField(
                choices=[
                    ("not_related", "Not related"),
                    ("unlikely_related", "Unlikely related"),
                    ("possibly_related", "Possibly related"),
                    ("probably_related", "Probably related"),
                    ("definitely_related", "Definitely related"),
                    ("N/A", "Not applicable"),
                ],
                default="-",
                max_length=25,
                verbose_name="Relationship to study drugs: Flucytosine:",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="aeinitial",
            name="inpatient_status",
            field=models.CharField(
                choices=[
                    ("inpatient", "Currently an inpatient"),
                    ("discharged", "Discharged"),
                    ("dead", "Died during hospitalization"),
                    ("N/A", "Not applicable"),
                ],
                default="-",
                max_length=25,
                verbose_name="Inpatient status:",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="aeinitial",
            name="patient_admitted",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="-",
                max_length=15,
                verbose_name="Was the patient admitted?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalaeinitial",
            name="date_admitted",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name='If "Yes", please specify date of hospital admission:',
            ),
        ),
        migrations.AddField(
            model_name="historicalaeinitial",
            name="date_discharged",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name='If "Discharged", please specify date discharged:',
            ),
        ),
        migrations.AddField(
            model_name="historicalaeinitial",
            name="fluconazole_relation",
            field=models.CharField(
                choices=[
                    ("not_related", "Not related"),
                    ("unlikely_related", "Unlikely related"),
                    ("possibly_related", "Possibly related"),
                    ("probably_related", "Probably related"),
                    ("definitely_related", "Definitely related"),
                    ("N/A", "Not applicable"),
                ],
                default="-",
                max_length=25,
                verbose_name="Relationship to study drugs: Fluconazole:",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalaeinitial",
            name="flucytosine_relation",
            field=models.CharField(
                choices=[
                    ("not_related", "Not related"),
                    ("unlikely_related", "Unlikely related"),
                    ("possibly_related", "Possibly related"),
                    ("probably_related", "Probably related"),
                    ("definitely_related", "Definitely related"),
                    ("N/A", "Not applicable"),
                ],
                default="-",
                max_length=25,
                verbose_name="Relationship to study drugs: Flucytosine:",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalaeinitial",
            name="inpatient_status",
            field=models.CharField(
                choices=[
                    ("inpatient", "Currently an inpatient"),
                    ("discharged", "Discharged"),
                    ("dead", "Died during hospitalization"),
                    ("N/A", "Not applicable"),
                ],
                default="-",
                max_length=25,
                verbose_name="Inpatient status:",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalaeinitial",
            name="patient_admitted",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="-",
                max_length=15,
                verbose_name="Was the patient admitted?",
            ),
            preserve_default=False,
        ),
    ]
