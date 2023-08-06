# Generated by Django 2.2.28 on 2023-03-27 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_tzcld', '0006_auto_20230327_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='tzcldcommunity',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='region', to='djangoldp_tzcld.TzcldTerritoryRegion'),
        ),
        migrations.AddField(
            model_name='tzcldprofile',
            name='membership',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='membership', to='djangoldp_tzcld.TzcldProfilesMembership'),
        ),
    ]
