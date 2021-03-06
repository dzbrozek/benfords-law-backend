import csv
import io
import logging
from collections import Counter
from csv import Dialect
from typing import Dict, Iterable, Optional, Type, Union, cast

from datasets.models import DataSet
from drf_extra_fields.fields import Base64FileField
from rest_framework import serializers

logger = logging.getLogger(__name__)


class CSVBase64File(Base64FileField):
    ALLOWED_TYPES = ['csv']

    def get_file_extension(self, filename: str, decoded_file: bytes) -> str:
        return 'csv'


def calc_distribution(reader: Iterable[dict], column_name: str) -> Dict[int, int]:
    leading_numbers = []

    for row in reader:
        try:
            value = row[column_name] if row[column_name] is not None else ''
            leading_numbers.append(int(value.replace('0', '').replace('.', '')[0]))
        except KeyError:
            raise serializers.ValidationError(f'Invalid column name: "{column_name}"')
        except (IndexError, ValueError) as e:
            logger.warning('Invalid value in column "%s". Value: %s. Error: %s', column_name, row[column_name], e)

    return {**dict([(x, 0) for x in range(1, 10)]), **dict(Counter(leading_numbers).items())}


class DataSetSerializer(serializers.ModelSerializer):
    column_name = serializers.CharField(write_only=True)
    file = CSVBase64File(write_only=True)

    class Meta:
        model = DataSet
        fields = ('id', 'name', 'created', 'distribution', 'file', 'column_name')
        read_only_fields = ('distribution',)

    def create(self, validated_data: dict) -> DataSet:
        column_name = validated_data.pop('column_name')
        try:
            csv_text = io.StringIO(validated_data.pop('file').read().decode('utf-8'))
        except UnicodeDecodeError:
            raise serializers.ValidationError('Invalid csv file')

        sniffer = csv.Sniffer()
        dialect: Optional[Union[str, Dialect, Type[Dialect]]] = None
        try:
            dialect = sniffer.sniff(csv_text.read(1024))
        except csv.Error:
            pass
        csv_text.seek(0)
        reader = csv.DictReader(csv_text, dialect=dialect)  # type: ignore

        data = {**validated_data, 'distribution': calc_distribution(reader, column_name)}

        return cast(DataSet, super().create(data))
