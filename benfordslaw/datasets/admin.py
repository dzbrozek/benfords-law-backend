from datasets.models import DataSet
from django.contrib import admin


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
