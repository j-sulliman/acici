# Generated by Django 2.1.7 on 2019-03-20 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nxos_config_import', '0002_nxos_vlan_svi'),
    ]

    operations = [
        migrations.AddField(
            model_name='nxos_vlan_svi',
            name='hostname',
            field=models.CharField(default='none', max_length=200),
        ),
    ]
