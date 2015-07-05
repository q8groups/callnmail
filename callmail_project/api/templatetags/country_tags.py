from django import template

from api.models import Country

register = template.Library()


def country_code_prefix():
    country = Country.objects.all().order_by('priority')
    for c in country:
        c.prefix_val = c.prefix[1:]
    return country

register.assignment_tag(country_code_prefix)