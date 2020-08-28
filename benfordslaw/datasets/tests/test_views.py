from datasets.factories import DataSetFactory
from datasets.models import DataSet
from datasets.serializers import DataSetSerializer
from django.urls import reverse
from rest_framework.test import APITestCase


class DataSetsAPIViewGetTestCase(APITestCase):
    def test_get_data_sets(self):
        data_sets = DataSetFactory.create_batch(2)

        response = self.client.get(reverse('datasets-api'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), DataSetSerializer(data_sets[::-1], many=True).data)


class DataSetsAPIViewPostTestCase(APITestCase):
    def test_create_new_data_set(self):
        data = {'name': 'Test dataset', 'column_name': 'year', 'file': 'eWVhcgoyMDAwCjIwMTUKMTY1Ngo='}

        response = self.client.post(reverse('datasets-api'), data=data)

        data_set = DataSet.objects.get()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), DataSetSerializer(data_set).data)


class DataSetDetailsAPIViewGetTestCase(APITestCase):
    def test_get_data_set(self):
        data_set = DataSetFactory()

        response = self.client.get(reverse('dataset-api', kwargs=dict(dataset_id=data_set.pk)))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), DataSetSerializer(data_set).data)
