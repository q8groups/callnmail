# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0005_auto_20140918_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='age_group',
            field=models.CharField(max_length=10, choices=[(b'1-5', b'1-5'), (b'6-14', b'6-14'), (b'15-25', b'15-25'), (b'25-45', b'25-45'), (b'45+', b'45+')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='age_group',
            field=models.CharField(help_text=b'Age groups are: 1-5, 6-14, 15-25, 25-45, 45+', max_length=10, choices=[(b'1-5', b'1-5'), (b'6-14', b'6-14'), (b'15-25', b'15-25'), (b'25-45', b'25-45'), (b'45+', b'45+')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(help_text=b'M for Male F for Female', max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')]),
        ),
    ]
