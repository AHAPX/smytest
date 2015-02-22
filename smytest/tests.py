from django.conf import settings
from django.test import Client
from unittest import TestCase
from django.core.urlresolvers import reverse
from smytest.models import MODELS, getModelsList
import yaml, json
import random

client = Client()
data = yaml.load(open(settings.TESTDATA_FILE))


class DynamicModelTests (TestCase):

    def test_get_models (self):
        model_list = json.loads(client.get(reverse('models_list')).content)['models']
        self.assertEqual(model_list, getModelsList())

    def test2_add_data (self):
        for name, records in data.iteritems():
            count = 0;
            for record in records:
                record.update({'model_name': name})
                response = client.post(reverse('add'), record)
                self.assertIn('success', response.content) and self.assertTrue(response.content['success'])
                count += 1;
            self.assertEqual(len(json.loads(client.post(reverse('model'), {'name': name}).content)['data']), count)

    def test3_modify_data (self):
        for model in getModelsList():
            model_data = json.loads(client.post(reverse('model'), {'name': model['name']}).content)
            head = model_data['head']
            record = random.choice(model_data['data'])
            for field in head:
                if 'type' in field and field['type'] in ('text', 'number'):
                    if field['type'] == 'text':
                        record[field['name']] += ' changed'
                    else:
                        record[field['name']] += 13
                    response = client.post(reverse('modify'), {
                        'model_name': model['name'],
                        'id': record['id'],
                        'name': field['name'],
                        'value': record[field['name']]
                    })
                    self.assertIn('success', response.content) and self.assertTrue(response.content['success'])
            model_data = json.loads(client.post(reverse('model'), {'name': model['name']}).content)
            new_record = filter(lambda a: a['id'] == record['id'], model_data['data'])[0]
            self.assertEqual(record, new_record)


