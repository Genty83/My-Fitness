# Generated by Django 5.1.2 on 2024-11-12 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='half_star',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productreview',
            name='stars',
            field=models.IntegerField(default=0),
        ),
    ]
