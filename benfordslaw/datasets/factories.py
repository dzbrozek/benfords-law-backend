from typing import Dict

import factory.fuzzy
from datasets.models import DataSet
from faker import Faker


def distribution_factory() -> Dict[str, int]:
    fake = Faker()

    return {
        '1': fake.pyint(),
        '2': fake.pyint(),
        '3': fake.pyint(),
        '4': fake.pyint(),
        '5': fake.pyint(),
        '6': fake.pyint(),
        '7': fake.pyint(),
        '8': fake.pyint(),
        '9': fake.pyint(),
    }


class DataSetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DataSet

    name = factory.Faker('word')
    distribution = factory.LazyFunction(distribution_factory)
