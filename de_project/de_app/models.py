from django.db import models
from datetime import datetime

class Metric(models.Model):
    name = models.CharField(default="INVALID_METRIC")
    current_value = models.IntegerField(default=0)
    total_value = models.IntegerField(default=0)
    average_value = models.IntegerField(default=0)
    is_valid = False

    def __str__(self):
        return self.name

    def validate(self):
        #Other validation can be done here
        self.is_valid = True

    def reset(self):
        self.current_value = 0
        self.total_value = 0
        self.average_value = 0

class Record(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    location = models.CharField(default="")
    metrics = models.ManyToManyField(Metric)
    is_valid = False

    def validate(self):
        #Other validation can be done here
        self.is_valid = True

    def create_metrics(self, metric_names_to_create = []):
        for n in metric_names_to_create:
            toAdd = Metric(name=n)
            toAdd.validation()
            metrics.add(toAdd)

    def get_metric(self, metric_name):
        for m in self.metrics:
            if m.name == metric_name:
                return m
        return Metric()

    def do_metrics_contain(self, metrics):
        for m in metrics:
            if not get_metric(m.name).is_valid:
                return False
        return True
