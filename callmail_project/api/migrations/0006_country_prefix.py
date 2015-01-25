# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_country_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='prefix',
            field=models.CharField(default='', max_length=6, blank=True),
            preserve_default=False,
        ),
    ]
