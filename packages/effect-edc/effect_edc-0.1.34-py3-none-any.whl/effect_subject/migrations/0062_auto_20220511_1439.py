# Generated by Django 3.2.11 on 2022-05-11 11:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0061_auto_20220511_0546"),
    ]

    operations = [
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_abnormal",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                null=True,
                verbose_name="abnormal",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_diff_abnormal",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                null=True,
                verbose_name="abnormal",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_diff_grade",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (0, "Not graded"),
                    (1, "Grade 1"),
                    (2, "Grade 2"),
                    (3, "Grade 3"),
                    (4, "Grade 4"),
                    (5, "Grade 5"),
                ],
                null=True,
                verbose_name="Grade",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_diff_grade_description",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Grade description"
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_diff_reportable",
            field=models.CharField(
                blank=True,
                choices=[
                    ("N/A", "Not applicable"),
                    ("3", "Yes, grade 3"),
                    ("4", "Yes, grade 4"),
                    ("No", "Not reportable"),
                    ("Already reported", "Already reported"),
                    ("present_at_baseline", "Present at baseline"),
                ],
                max_length=25,
                null=True,
                verbose_name="reportable",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_diff_units",
            field=models.CharField(
                blank=True,
                choices=[("%", "%")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_diff_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="Lymphocyte (differential)",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_grade",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (0, "Not graded"),
                    (1, "Grade 1"),
                    (2, "Grade 2"),
                    (3, "Grade 3"),
                    (4, "Grade 4"),
                    (5, "Grade 5"),
                ],
                null=True,
                verbose_name="Grade",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_grade_description",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Grade description"
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_reportable",
            field=models.CharField(
                blank=True,
                choices=[
                    ("N/A", "Not applicable"),
                    ("3", "Yes, grade 3"),
                    ("4", "Yes, grade 4"),
                    ("No", "Not reportable"),
                    ("Already reported", "Already reported"),
                    ("present_at_baseline", "Present at baseline"),
                ],
                max_length=25,
                null=True,
                verbose_name="reportable",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_units",
            field=models.CharField(
                blank=True,
                choices=[("10^9/L", "10^9/L")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="lymphocyte_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="Lymphocyte (absolute)",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="neutrophil_diff_abnormal",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                null=True,
                verbose_name="abnormal",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="neutrophil_diff_grade",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (0, "Not graded"),
                    (1, "Grade 1"),
                    (2, "Grade 2"),
                    (3, "Grade 3"),
                    (4, "Grade 4"),
                    (5, "Grade 5"),
                ],
                null=True,
                verbose_name="Grade",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="neutrophil_diff_grade_description",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Grade description"
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="neutrophil_diff_reportable",
            field=models.CharField(
                blank=True,
                choices=[
                    ("N/A", "Not applicable"),
                    ("3", "Yes, grade 3"),
                    ("4", "Yes, grade 4"),
                    ("No", "Not reportable"),
                    ("Already reported", "Already reported"),
                    ("present_at_baseline", "Present at baseline"),
                ],
                max_length=25,
                null=True,
                verbose_name="reportable",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="neutrophil_diff_units",
            field=models.CharField(
                blank=True,
                choices=[("%", "%")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultsfbc",
            name="neutrophil_diff_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="Neutrophils",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_abnormal",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                null=True,
                verbose_name="abnormal",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_diff_abnormal",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                null=True,
                verbose_name="abnormal",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_diff_grade",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (0, "Not graded"),
                    (1, "Grade 1"),
                    (2, "Grade 2"),
                    (3, "Grade 3"),
                    (4, "Grade 4"),
                    (5, "Grade 5"),
                ],
                null=True,
                verbose_name="Grade",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_diff_grade_description",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Grade description"
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_diff_reportable",
            field=models.CharField(
                blank=True,
                choices=[
                    ("N/A", "Not applicable"),
                    ("3", "Yes, grade 3"),
                    ("4", "Yes, grade 4"),
                    ("No", "Not reportable"),
                    ("Already reported", "Already reported"),
                    ("present_at_baseline", "Present at baseline"),
                ],
                max_length=25,
                null=True,
                verbose_name="reportable",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_diff_units",
            field=models.CharField(
                blank=True,
                choices=[("%", "%")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_diff_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="Lymphocyte (differential)",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_grade",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (0, "Not graded"),
                    (1, "Grade 1"),
                    (2, "Grade 2"),
                    (3, "Grade 3"),
                    (4, "Grade 4"),
                    (5, "Grade 5"),
                ],
                null=True,
                verbose_name="Grade",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_grade_description",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Grade description"
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_reportable",
            field=models.CharField(
                blank=True,
                choices=[
                    ("N/A", "Not applicable"),
                    ("3", "Yes, grade 3"),
                    ("4", "Yes, grade 4"),
                    ("No", "Not reportable"),
                    ("Already reported", "Already reported"),
                    ("present_at_baseline", "Present at baseline"),
                ],
                max_length=25,
                null=True,
                verbose_name="reportable",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_units",
            field=models.CharField(
                blank=True,
                choices=[("10^9/L", "10^9/L")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="lymphocyte_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="Lymphocyte (absolute)",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="neutrophil_diff_abnormal",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                null=True,
                verbose_name="abnormal",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="neutrophil_diff_grade",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (0, "Not graded"),
                    (1, "Grade 1"),
                    (2, "Grade 2"),
                    (3, "Grade 3"),
                    (4, "Grade 4"),
                    (5, "Grade 5"),
                ],
                null=True,
                verbose_name="Grade",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="neutrophil_diff_grade_description",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Grade description"
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="neutrophil_diff_reportable",
            field=models.CharField(
                blank=True,
                choices=[
                    ("N/A", "Not applicable"),
                    ("3", "Yes, grade 3"),
                    ("4", "Yes, grade 4"),
                    ("No", "Not reportable"),
                    ("Already reported", "Already reported"),
                    ("present_at_baseline", "Present at baseline"),
                ],
                max_length=25,
                null=True,
                verbose_name="reportable",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="neutrophil_diff_units",
            field=models.CharField(
                blank=True,
                choices=[("%", "%")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultsfbc",
            name="neutrophil_diff_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9999),
                ],
                verbose_name="Neutrophils",
            ),
        ),
    ]
