# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_auto_20140610_0659'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mail', models.ForeignKey(to='mail.Mail', to_field='id')),
                ('attachment', models.FileField(upload_to=b'attachments/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
