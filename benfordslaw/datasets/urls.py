from datasets.views import DataSetDetailsAPIView, DataSetsAPIView
from django.urls import path

urlpatterns = [
    path('data-sets/', DataSetsAPIView.as_view(), name='datasets-api'),
    path('data-sets/<int:dataset_id>/', DataSetDetailsAPIView.as_view(), name='dataset-api'),
]
