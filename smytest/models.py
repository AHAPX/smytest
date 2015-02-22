# coding: utf8

from django.db import models
from django.conf import settings
from rest_framework import serializers
from django import forms
import yaml

TYPES = {
    'int': models.IntegerField,
    'char': models.CharField,
    'date': models.DateField,
}

TYPES_SER = {
    'int': serializers.IntegerField,
    'char': serializers.CharField,
    'date': serializers.DateField,
}

TYPES_FORM = {
    'int': forms.IntegerField,
    'char': forms.CharField,
    'date': forms.DateField,
}

PARAMS = {
    'int': {},
    'char': {'max_length': 100},
    'date': {},
}

HTMLTYPES = {
    'int': 'number',
    'char': 'text',
    'date': 'date',
}

MODELS = []

def createTable (name, title, fields):

    attrs = {'__module__': 'smytest.models'}
    attrs_ser = {'id': serializers.IntegerField()}
    attrs_form = {}
    head_attrs = [{'name': 'id', 'title': 'id'}]
    for field in fields:
        attrs.update({
            field['id']: TYPES[field['type']](**PARAMS[field['type']])
        })
        attrs_ser.update({
            field['id']: TYPES_SER[field['type']](**PARAMS[field['type']])
        })
        attrs_form.update({
            field['id']: TYPES_FORM[field['type']](**PARAMS[field['type']])
        })
        head_attrs += [{
            'name': field['id'],
            'title': field['title'],
            'type': HTMLTYPES[field['type']],
        }]
    return {
        'name': name,
        'model': type(name, (models.Model,), attrs),
        'title': title,
        'serializer': type('{0}Serializer'.format(name), (serializers.Serializer,), attrs_ser),
        'form': type('{0}Form'.format(name), (forms.Form,), attrs_form),
        'head': head_attrs,
    }

def getModelsList ():
    return map(lambda a: {'name': a['name'], 'title': a['title']}, MODELS)

def getModel (name):
    for m in MODELS:
        if m['name'] == name:
            return m
    return None


scheme = yaml.load(open(settings.SCHEME_FILE))
for table in scheme.iteritems():
    MODELS += [createTable(table[0], table[1]['title'], table[1]['fields'])]

