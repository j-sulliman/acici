# Generated by Django 2.1.7 on 2019-03-25 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nxos_config_import', '0013_auto_20190325_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fvaepg',
            name='fvSubnet',
            field=models.GenericIPAddressField(),
        ),
    ]