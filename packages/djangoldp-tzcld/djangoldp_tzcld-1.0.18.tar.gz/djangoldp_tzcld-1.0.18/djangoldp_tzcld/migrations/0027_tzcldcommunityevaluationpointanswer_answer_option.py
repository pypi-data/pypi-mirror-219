# Generated by Django 2.2.28 on 2023-07-03 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_tzcld', '0026_auto_20230703_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='tzcldcommunityevaluationpointanswer',
            name='answer_option',
            field=models.CharField(blank=True, default='', max_length=1024, null=True),
        ),
    ]
