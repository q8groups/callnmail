from django.db import models
from tinymce import models as tinymce_models


class StaticContents(models.Model):
    title = models.CharField(max_length=255)
    body = tinymce_models.HTMLField()
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title




