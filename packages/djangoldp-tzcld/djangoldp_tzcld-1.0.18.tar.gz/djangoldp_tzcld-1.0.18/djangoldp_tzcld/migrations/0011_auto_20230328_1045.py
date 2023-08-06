# Generated by Django 2.2.28 on 2023-03-28 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_tzcld', '0010_auto_20230327_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tzcldjobsphones',
            name='job',
        ),
        migrations.RemoveField(
            model_name='tzcldjobsphones',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='tzcldterritoriesemails',
            name='email',
        ),
        migrations.RemoveField(
            model_name='tzcldterritoriesemails',
            name='job',
        ),
        migrations.RemoveField(
            model_name='tzcldterritorieslocations',
            name='location',
        ),
        migrations.RemoveField(
            model_name='tzcldterritorieslocations',
            name='tzcld_community',
        ),
        migrations.RemoveField(
            model_name='tzcldterritoriesphones',
            name='job',
        ),
        migrations.RemoveField(
            model_name='tzcldterritoriesphones',
            name='phone',
        ),
        migrations.AlterModelOptions(
            name='tzcldcontactemail',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control'], 'verbose_name': 'TZCLD email', 'verbose_name_plural': 'TZCLD emails'},
        ),
        migrations.AlterModelOptions(
            name='tzcldcontactphone',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control'], 'verbose_name': 'TZCLD phone', 'verbose_name_plural': 'TZCLD phones'},
        ),
        migrations.AlterModelOptions(
            name='tzcldterritorylocation',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control'], 'verbose_name': 'TZCLD Territory location', 'verbose_name_plural': 'TZCLD Territories locations'},
        ),
        migrations.RemoveField(
            model_name='tzcldcommunity',
            name='locations',
        ),
        migrations.RemoveField(
            model_name='tzcldprofilejob',
            name='emails',
        ),
        migrations.RemoveField(
            model_name='tzcldprofilejob',
            name='phones',
        ),
        migrations.RemoveField(
            model_name='tzcldterritorylocation',
            name='emails',
        ),
        migrations.RemoveField(
            model_name='tzcldterritorylocation',
            name='phones',
        ),
        migrations.AddField(
            model_name='tzcldcontactemail',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='djangoldp_tzcld.TzcldProfileJob'),
        ),
        migrations.AddField(
            model_name='tzcldcontactemail',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='djangoldp_tzcld.TzcldTerritoryLocation'),
        ),
        migrations.AddField(
            model_name='tzcldcontactphone',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='djangoldp_tzcld.TzcldProfileJob'),
        ),
        migrations.AddField(
            model_name='tzcldcontactphone',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='djangoldp_tzcld.TzcldTerritoryLocation'),
        ),
        migrations.AddField(
            model_name='tzcldterritorylocation',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='djangoldp_tzcld.TzcldCommunity'),
        ),
        migrations.DeleteModel(
            name='TzcldJobsEmails',
        ),
        migrations.DeleteModel(
            name='TzcldJobsPhones',
        ),
        migrations.DeleteModel(
            name='TzcldTerritoriesEmails',
        ),
        migrations.DeleteModel(
            name='TzcldTerritoriesLocations',
        ),
        migrations.DeleteModel(
            name='TzcldTerritoriesPhones',
        ),
    ]
