# Generated by Django 2.0.4 on 2018-05-02 11:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20180502_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 2, 19, 53, 5, 141625), verbose_name='发送事件'),
        ),
    ]
