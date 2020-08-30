from datasets.serializers import DataSetSerializer, calc_distribution
from django.test import TestCase
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail


class DataSetSerializerTest(TestCase):
    def test_empty_data(self):
        data = {}

        serializer = DataSetSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertDictEqual(
            serializer.errors,
            {
                'column_name': [ErrorDetail(string='This field is required.', code='required')],
                'file': [ErrorDetail(string='No file was submitted.', code='required')],
                'name': [ErrorDetail(string='This field is required.', code='required')],
            },
        )

    def test_invalid_column_name(self):
        data = {'name': 'Test dataset', 'column_name': 'unknown', 'file': 'eWVhcgoyMDAwCjIwMTUKMTY1Ngo='}

        serializer = DataSetSerializer(data=data)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        with self.assertRaises(serializers.ValidationError) as cm:
            serializer.save()

        self.assertEqual(cm.exception.detail, [ErrorDetail(string='Invalid column name: "unknown"', code='invalid')])

    def test_invalid_file(self):
        data = {
            'name': 'Test dataset',
            'column_name': 'unknown',
            'file': 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==',
        }

        serializer = DataSetSerializer(data=data)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        with self.assertRaises(serializers.ValidationError) as cm:
            serializer.save()

        self.assertEqual(cm.exception.detail, [ErrorDetail(string='Invalid csv file', code='invalid')])

    def test_create_dataset(self):
        data = {'name': 'Test dataset', 'column_name': 'year', 'file': 'eWVhcgoyMDAwCjIwMTUKMTY1Ngo='}

        serializer = DataSetSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

        data_set = serializer.save()

        self.assertEqual(data_set.name, data['name'])
        self.assertTrue(data_set.created)
        self.assertDictEqual(data_set.distribution, {2: 2, 1: 1})


class CalcDistributionTestCase(TestCase):
    def setUp(self):
        self.reader = [
            {'name': 'First', 'value': '1.23'},
            {'name': 'Second', 'value': '45'},
            {'name': 'Third', 'value': '0.63'},
            {'name': 'Fourth', 'value': 'zero'},
            {'name': 'Fifth', 'value': '123'},
            {'name': 'Sixth', 'value': None},
        ]

    def test_calc_distribution(self):
        self.assertDictEqual(
            calc_distribution(self.reader, 'value'), {1: 2, 2: 0, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 0, 9: 0}
        )

    def test_unknown_column(self):
        with self.assertRaises(serializers.ValidationError) as cm:
            calc_distribution(self.reader, 'unknown')

        self.assertEqual(cm.exception.detail, [ErrorDetail(string='Invalid column name: "unknown"', code='invalid')])
