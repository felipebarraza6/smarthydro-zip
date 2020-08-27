# Generated by Django 2.1.4 on 2019-01-29 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('api', '0002_sensor_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lectura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recibido', models.DateTimeField(auto_now_add=True)),
                ('medido', models.DateTimeField(blank=True)),
                ('valor', models.FloatField(default=-1270.0)),
            ],
            options={
                'ordering': ('recibido',),
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('grupo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proyectos', to='auth.Group')),
                ('propietario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proyectos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Unidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abreviacion', models.CharField(max_length=100, unique=True)),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField()),
            ],
            options={
                'ordering': ('creado',),
            },
        ),
        migrations.AlterModelOptions(
            name='sensor',
            options={'ordering': ('creado',)},
        ),
        migrations.RenameField(
            model_name='sensor',
            old_name='created',
            new_name='creado',
        ),
        migrations.RenameField(
            model_name='sensor',
            old_name='description',
            new_name='descripcion',
        ),
        migrations.RenameField(
            model_name='sensor',
            old_name='name',
            new_name='nombre',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='unit',
        ),
        migrations.AddField(
            model_name='sensor',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sensor',
            name='fabricante',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='sensor',
            name='link',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='lectura',
            name='sensor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lecturas', to='api.Sensor'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='proyecto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sensores', to='api.Proyecto'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='unidad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sensores', to='api.Unidad'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='variable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sensores', to='api.Variable'),
        ),
    ]