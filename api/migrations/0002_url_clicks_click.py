# Generated by Django 4.2.13 on 2024-06-05 19:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='clicks',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ip_address', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=50)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.url')),
            ],
        ),
    ]
