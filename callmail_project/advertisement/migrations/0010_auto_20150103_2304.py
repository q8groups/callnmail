# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0009_auto_20141201_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='gender',
            field=models.CharField(max_length=1, choices=[(b'', b'Not Set'), (b'M', b'Male'), (b'F', b'Female')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, help_text=b'M for Male F for Female', max_length=1, choices=[(b'', b'Not Set'), (b'M', b'Male'), (b'F', b'Female')]),
        ),
    ]
