# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='age_group',
            field=models.CharField(default=-8, max_length=10, choices=[(b'1-5', b'1, 2, 3, 4, 5'), (b'6-14', b'6-14'), (b'15-25', b'15-25'), (b'25-45', b'25-45'), (b'45-', b'45+')]),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='advertisement',
            name='age_group',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='age',
        ),
    ]
