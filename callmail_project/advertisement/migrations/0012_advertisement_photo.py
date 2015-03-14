# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0011_auto_20150226_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='photo',
            field=models.ImageField(default='', upload_to=b'ads/', blank=True),
            preserve_default=False,
        ),
    ]
