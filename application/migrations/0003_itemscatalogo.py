# Generated by Django 2.1.7 on 2019-05-05 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_auto_20190504_1704'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemsCatalogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]