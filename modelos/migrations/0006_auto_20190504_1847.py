# Generated by Django 2.1.7 on 2019-05-04 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0005_auto_20190504_1834'),
    ]

    operations = [
        migrations.CreateModel(
            name='Puja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('monto', models.FloatField()),
                ('fecha_y_hora', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='subasta',
            name='id',
        ),
        migrations.AddField(
            model_name='subasta',
            name='codigo',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='puja',
            name='codigo_subasta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modelos.Subasta'),
        ),
    ]