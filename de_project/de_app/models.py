from django.db import models
from datetime import datetime

class Metric(models.Model):
    name = models.CharField(default="INVALID_METRIC", max_length=255)
    current_value = models.IntegerField(default=0)
    total_value = models.IntegerField(default=0)
    average_value = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def validate(self):
        #Other validation can be done here
        self.save()

    def reset(self):
        self.current_value = 0
        self.total_value = 0
        self.average_value = 0

    def get_metric(metric_name, metrics):
        for m in metrics:
            if m.name == metric_name:
                return m
        raise ValueError("No Metric {metric_name} in {metrics}")

class Record(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    location = models.CharField(default="", max_length=255)
    metrics = models.ManyToManyField(Metric)

    def validate(self):
        #Other validation can be done here
        self.save()

    def create_metrics(self, metric_names_to_create = []):
        for n in metric_names_to_create:
            toAdd = Metric(name=n)
            toAdd.validate()
            self.metrics.add(toAdd)

    def get_metric(self, metric_name):
        return Metric.get_metric(metric_name, self.metrics.all())

    def do_metrics_contain(self, metrics):
        for m in metrics:
            if self.get_metric(m.name).name == "INVALID_METRIC":
                return False
        return True
