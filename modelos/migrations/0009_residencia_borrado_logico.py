# Generated by Django 2.1.7 on 2019-05-04 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0008_alquila'),
    ]

    operations = [
        migrations.AddField(
            model_name='residencia',
            name='borrado_logico',
            field=models.BooleanField(default=False),
        ),
    ]
