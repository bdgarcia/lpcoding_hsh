# Generated by Django 2.1.7 on 2019-05-05 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0014_auto_20190504_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='residencia',
            name='foto',
            field=models.FilePathField(blank=True, default=None, null=True),
        ),
    ]