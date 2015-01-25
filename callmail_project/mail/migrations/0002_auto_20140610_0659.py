# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mail',
            old_name='date',
            new_name='date_email',
        ),
    ]
