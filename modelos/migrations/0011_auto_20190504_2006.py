# Generated by Django 2.1.7 on 2019-05-04 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0010_auto_20190504_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='residencia',
            name='foto',
            field=models.FileField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]