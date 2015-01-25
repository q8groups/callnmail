# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mail', '0003_mailattachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForgotPasswordToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('secret_token', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
