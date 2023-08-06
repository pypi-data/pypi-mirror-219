# Generated by Django 2.2.28 on 2023-04-06 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_community', '0011_auto_20220711_0837'),
        ('djangoldp_tzcld', '0016_tzcldcontactmember'),
    ]

    operations = [
        migrations.AddField(
            model_name='tzcldcontactmember',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tzcld_community_contacts', to='djangoldp_community.Community'),
        ),
    ]
