# Generated by Django 2.0.4 on 2018-05-25 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owtd', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
