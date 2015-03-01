from django import template

from api.models import Country

register = template.Library()


def country_code_prefix():
    prefix = Country.objects.all().order_by('priority').values_list('prefix')
    return [''.join(i) for i in prefix]

register.assignment_tag(country_code_prefix)