# Generated by Django 3.2.9 on 2021-11-19 16:37

import edc_model.validators.date
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_screening", "0003_auto_20211118_2214"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalsubjectscreening",
            name="csf_cm_date",
        ),
        migrations.RemoveField(
            model_name="historicalsubjectscreening",
            name="prior_cm_epidose_date",
        ),
        migrations.RemoveField(
            model_name="subjectscreening",
            name="csf_cm_date",
        ),
        migrations.RemoveField(
            model_name="subjectscreening",
            name="prior_cm_epidose_date",
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="cd4_date",
            field=models.DateField(
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Most recent CD4 count sample collection date",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="csf_cm_value",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("NO_FURTHER_TESTS", "No, No further testing done on CSF"),
                    ("PENDING", "Pending"),
                    ("N/A", "Not applicable"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                help_text="i.e. positive microscopy with India Ink, culture, or CrAg test) at any time between the CrAg test and screening for eligibility, or during the first 2 weeks of antifungal treatment, while the patient remained without clinical symptoms/ signs of meningitis. See also CSF CrAg value above. (late withdrawal criterion).",
                max_length=25,
                verbose_name="Any other evidence of CM on CSF?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="on_fluconazole",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("not_answered", "Not answered")],
                default="not_answered",
                help_text="fluconazole @ (800-1200 mg/day)",
                max_length=25,
                verbose_name="Has the patient taken 7 or more doses of high-dose fluconazole treatment in the last 7 days?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="cd4_date",
            field=models.DateField(
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Most recent CD4 count sample collection date",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="csf_cm_value",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("NO_FURTHER_TESTS", "No, No further testing done on CSF"),
                    ("PENDING", "Pending"),
                    ("N/A", "Not applicable"),
                    ("not_answered", "Not answered"),
                ],
                default="not_answered",
                help_text="i.e. positive microscopy with India Ink, culture, or CrAg test) at any time between the CrAg test and screening for eligibility, or during the first 2 weeks of antifungal treatment, while the patient remained without clinical symptoms/ signs of meningitis. See also CSF CrAg value above. (late withdrawal criterion).",
                max_length=25,
                verbose_name="Any other evidence of CM on CSF?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="on_fluconazole",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("not_answered", "Not answered")],
                default="not_answered",
                help_text="fluconazole @ (800-1200 mg/day)",
                max_length=25,
                verbose_name="Has the patient taken 7 or more doses of high-dose fluconazole treatment in the last 7 days?",
            ),
        ),
    ]
