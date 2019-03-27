# Generated by Django 2.1.7 on 2019-03-21 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nxos_config_import', '0007_epginputform_migration_leafs_nodeid'),
    ]

    operations = [
        migrations.CreateModel(
            name='PushDataApic',
            fields=[
                ('apic_addr', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='epginputform',
            name='apic_addr',
            field=models.GenericIPAddressField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='epginputform',
            name='migration_leafs_nodeid',
            field=models.CharField(default='101-102', max_length=200),
        ),
    ]