from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from django.shortcuts import render_to_response
from smytest.models import MODELS, getModelsList, getModel
import json


class MainViewSet(viewsets.ViewSet):

    def message (self, msg):
        return Response(msg)

    def error (self, msg):
        return self.message({'error': msg})

    def success (self):
        return self.message({'success': True})

    def error_form (self, form):
        errors = []
        for key, value in form.errors.iteritems():
            errors += [{'field': key, 'text': value.as_text()}]
        return self.error(errors)

    def get_models (self, request):
        return self.message({'models': getModelsList()})

    def get_model (self, request, *args, **kwargs):
        dyn_model = getModel(request.DATA['name'])
        if dyn_model:
            result = dyn_model['serializer'](dyn_model['model'].objects.all(), many = True).data
            return self.message({
                'head': dyn_model['head'],
                'data': result
            })
        return self.error('model not found')

    def add_new (self, request, *args, **kwargs):
        dyn_model = getModel(request.DATA['model_name'])
        if dyn_model:
            form = dyn_model['form'](request.DATA)
            if form.is_valid():
                dyn_model['model'].objects.create(**form.cleaned_data)
                return self.success()
            return self.error_form(form)
        return self.error('model not found')            

    def modify (self, request, *args, **kwargs):
        dyn_model = getModel(request.DATA['model_name'])
        field_name = request.DATA['name']
        pk = request.DATA['id']
        value = request.DATA['value']
        try:
            record = dyn_model['model'].objects.get(pk = pk)
            setattr(record, field_name, value)
            record.save()
            return self.success()
        except dyn_model['model'].DoesNotExist:
            return self.error('record not found')


def indexView (request):
    return render_to_response('index.html')
