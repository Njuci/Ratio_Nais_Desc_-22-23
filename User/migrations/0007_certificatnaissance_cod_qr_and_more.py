# Generated by Django 4.2.5 on 2023-10-23 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_certificat_desc_date_deliv_cert'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificatnaissance',
            name='cod_qr',
            field=models.ImageField(null=True, upload_to='certificat_naissance'),
        ),
        migrations.AddField(
            model_name='certificatnaissance',
            name='url_qrcode',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
