# Generated by Django 4.1.6 on 2023-04-12 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hives', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CriticalSituationsModel',
            fields=[
                ('hive', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='hives.hive')),
                ('is_swarming', models.BooleanField(default=False)),
                ('is_robbed', models.BooleanField(default=False)),
                ('is_robber', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HiveDetectorModel',
            fields=[
                ('hive', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='hives.hive')),
                ('obj', models.BinaryField(max_length=2000)),
            ],
        ),
    ]
