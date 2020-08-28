from datasets.models import DataSet
from datasets.serializers import DataSetSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView


class DataSetsAPIView(ListAPIView, CreateAPIView):
    queryset = DataSet.objects.all().order_by('-created')
    serializer_class = DataSetSerializer


class DataSetDetailsAPIView(RetrieveAPIView):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
    lookup_url_kwarg = 'dataset_id'
