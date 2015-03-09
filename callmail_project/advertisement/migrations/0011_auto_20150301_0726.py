# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0010_auto_20150103_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='photo',
            field=models.ImageField(default=1, upload_to=b'ads/', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default=b'default.png', upload_to=b'avatar/', blank=True),
        ),
    ]
