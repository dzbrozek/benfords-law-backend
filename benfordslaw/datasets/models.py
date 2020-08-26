from django.db import models


class DataSet(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    distribution = models.JSONField(default=dict)  # type: ignore

    def __str__(self) -> str:
        return self.name
