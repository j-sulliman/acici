# Generated by Django 2.1.7 on 2019-03-25 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nxos_config_import', '0011_auto_20190325_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='epginputform',
            name='bd_mode',
            field=models.CharField(default='l2', max_length=200),
        ),
        migrations.AddField(
            model_name='pushdataapic',
            name='user',
            field=models.CharField(default='admin', max_length=200),
        ),
    ]