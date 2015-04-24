from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from tinymce import models as tinymce_models

GENDER = [
    ('', 'Not Set'),
    ('M', 'Male'),
    ('F', 'Female')
]

AGE_GROUP = [
    ('1-5', '1-5'),
    ('6-14', '6-14'),
    ('15-25', '15-25'),
    ('25-45', '25-45'),
    ('45+', '45+')
]


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=1, choices=GENDER, help_text="M for Male F for Female", blank=True)
    age = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatar/", default='default.png', blank=True)
    # age_group = models.CharField(max_length=10, choices=AGE_GROUP, help_text="Age groups are: 1-5, 6-14, 15-25, ""25-45, 45+")
    country = CountryField(help_text="Country names are taken from the official ISO 3166-1 list. "
                                     "See: http://en.wikipedia.org/wiki/ISO_3166-1")


class Advertisement(models.Model):
    country = CountryField()
    gender = models.CharField(max_length=1, choices=GENDER)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP)
    body = tinymce_models.HTMLField()
    default = models.BooleanField(default=False, unique=True)
    photo = models.ImageField(upload_to="ads/", blank=True)

    def __unicode__(self):
        return '%s %s %s' % (self.country, self.gender, self.age_group)

    class Meta:
        unique_together = ('country', 'gender', 'age_group')



class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="banners/")


    def __unicode__(self):
        return self.title

