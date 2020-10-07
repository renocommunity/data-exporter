from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

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

class MetricSerializer(serializers.ModelSerializer):

    class Meta:
        model = Metric
        fields = ["name", "current_value", "total_value", "average_value"]


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
        return Metric.get_metric(metric_name, self.get_all_metrics())

    def get_all_metrics(self):
        return self.metrics.all()

    def do_metrics_contain(self, metrics):
        for m in metrics:
            if self.get_metric(m.name).name == "INVALID_METRIC":
                return False
        return True

class RecordSerializer(serializers.ModelSerializer):
    metrics = MetricSerializer(read_only=True, many=True)

    class Meta:
        model = Record
        #We'll ignore location for now.
        fields = ["timestamp", "metrics"]

    #Flatten the metrics for easier use in tables.
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        metrics_representation = representation.pop('metrics')
        for m in metrics_representation:
            prefix = m.get('name') + '_'
            for val in [ 'current_value', 'total_value', 'average_value' ]:
                repkey = prefix + val
                representation[repkey] = m.get(val)


        return representation



class RecordHandler(models.Model):
    records = models.ManyToManyField(Record)
    metric_names = ArrayField(models.CharField(max_length=255))
    name = models.CharField(default="Record_Handler", max_length=255)

    def initialize(self):
        self.save()
        self.create_metrics_buffer()

    def create_metrics_buffer(self):
        self.metrics_buffer = [ Metric(name=n) for n in self.metric_names ]
        # print("RecordHandler metrics: " + serializers.serialize('json', self.metrics_buffer))

    #Create a record with metrics matching those in *this
    def create_record(self):
        ret = Record()
        ret.validate()
        ret.create_metrics([m.name for m in self.metrics_buffer])
        return ret

    def get_last_record(self):
        if self.get_all_records():
            return self.get_all_records()[-1]
        raise ValueError("No Existing Records")

    #Add a record to *this
    def add_record(self, record):
        if not record.do_metrics_contain(self.metrics_buffer):
            raise ValueError("Data shape mismatch")

        try:
            last_record_metrics = self.get_last_record().metrics
        except ValueError:
            last_record_metrics = self.metrics_buffer
        for m in self.metrics_buffer:
            current_metric = record.get_metric(m.name)
            #skipping validity checks because we can do that.
            current_metric.total_value = Metric.get_metric(m.name, last_record_metrics).total_value + current_metric.current_value
        self.records.add(record)

    def save_records(self):
        for r in self.get_all_records():
            r.save()

    def get_all_records(self):
        return self.records.all()

    def get_records_as_json(self):
        return JSONRenderer().render(RecordHandlerSerializer(self).data)

    def clean_data(self):
        #TODO: Sort data?
        pass

    def calculate_trends(self, bin_days=7):
        self.clean_data() # needs to be done first
        
        #calculate moving average of bin_days
        for r in self.get_all_records():
            first_record_timestamp = r.timestamp - timedelta(days = bin_days)
            #TODO: this will be slow on large data sets.
            record_subset = [ r for r in self.get_all_records() if r.timestamp > first_record_timestamp and r.timestamp <= r.timestamp ]
            for m in self.metrics_buffer:
                m.reset()
                for s in record_subset:
                    m.total_value += s.get_metric(m.name).current_value
                current_metric = r.get_metric(m.name)
                current_metric.average_value = current_metric.current_value
                if m.total_value:
                     current_metric.average_value /= m.total_value

class RecordHandlerSerializer(serializers.ModelSerializer):
    records = RecordSerializer(read_only=True, many=True)

    class Meta:
        model = RecordHandler
        fields = ["name", "records"]
