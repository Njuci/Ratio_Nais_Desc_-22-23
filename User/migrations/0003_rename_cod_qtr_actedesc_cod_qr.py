# Generated by Django 4.2.5 on 2023-10-30 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_rename_cod_qr_actedesc_cod_qtr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actedesc',
            old_name='cod_qtr',
            new_name='cod_qr',
        ),
    ]
