# Generated by Django 2.1.7 on 2019-05-06 14:11

from django.db import migrations, models
import django.db.models.deletion
import modelos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alquila',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('precio', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Puja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('monto', models.FloatField()),
                ('fecha_y_hora', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Residencia',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('ubicacion', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField()),
                ('precio', models.FloatField()),
                ('monto_minimo_subasta', models.FloatField()),
                ('foto', models.FileField(blank=True, default=None, null=True, upload_to=modelos.models.get_file_path)),
                ('borrado_logico', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subasta',
            fields=[
                ('monto_actual', models.FloatField()),
                ('monto_inicial', models.FloatField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_residencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelos.Residencia')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('contraseña', models.CharField(max_length=30)),
                ('tarjeta_credito', models.CharField(max_length=30)),
                ('creditos', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='puja',
            name='codigo_subasta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelos.Subasta'),
        ),
        migrations.AddField(
            model_name='alquila',
            name='codigo_residencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelos.Residencia'),
        ),
        migrations.AddField(
            model_name='alquila',
            name='email_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelos.Usuario'),
        ),
    ]
