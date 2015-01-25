# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0004_advertisement_age_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='age_group',
            field=models.CharField(max_length=10, choices=[(b'1-5', b'1-5'), (b'6-14', b'6-14'), (b'15-25', b'15-25'), (b'25-45', b'25-45'), (b'45-', b'45+')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='age_group',
            field=models.CharField(max_length=10, choices=[(b'1-5', b'1-5'), (b'6-14', b'6-14'), (b'15-25', b'15-25'), (b'25-45', b'25-45'), (b'45-', b'45+')]),
        ),
        migrations.AlterUniqueTogether(
            name='advertisement',
            unique_together=set([('country', 'gender', 'age_group')]),
        ),
    ]
