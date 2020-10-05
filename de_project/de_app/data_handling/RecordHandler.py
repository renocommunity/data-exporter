from ..models import Metric, Record
from django.core import serializers

class RecordHandler:
    def __init__(self, metric_names_to_create = []):
        self.records = []
        self.metrics_buffer = [ Metric(name=n) for n in metric_names_to_create ]
        print("RecordHandler metrics: " + serializers.serialize('json', self.metrics_buffer))

    #Create a record with metrics matching those in *this
    def create_record(self):
        ret = Record()
        ret.validate()
        ret.create_metrics([m.name for m in self.metrics_buffer])
        return ret

    def get_last_record(self):
        if self.records:
            return self.records[-1]
        raise ValueError("No Existing Records")

    #Add a record to *this
    def add_record(self, record):
        if not record.do_metrics_contain(self.metrics_buffer):
            raise ValueError("Data shape mismatch")

        try:
            last_record_metrics = self.get_last_record().metrics.all()
        except ValueError:
            last_record_metrics = self.metrics_buffer
        for m in self.metrics_buffer:
            current_metric = record.get_metric(m.name)
            #skipping validity checks because we can do that.
            current_metric.total_value = Metric.get_metric(m.name, last_record_metrics).total_value + current_metric.current_value
        self.records.append(record)

    def save_records(self):
        for r in self.records:
            r.save()

    def get_records_as_json(self):
        ret = serializers.serialize('json', self.records)
        return ret

    def clean_data(self):
        # self.records = [ r for r in self.records if r.is_valid ]
        self.records.sort(key=lambda r: r.timestamp)

    def calculate_trends(self, bin_days=7):
        self.clean_data() # needs to be done first
        
        #calculate moving average of bin_days
        for r in self.records:
            first_record_timestamp = r.timestamp - datetime.timedelta(days = bin_days)
            #TODO: this will be slow on large data sets.
            record_subset = [ r for r in self.records if r.timestamp > first_record_timestamp and r.timestamp <= r.timestamp ]
            for m in self.metrics_buffer:
                m.reset()
                for s in record_subset:
                    m.total_value += s.get_metric(m.name).current_value
                current_metric = r.get_metric(m.name)
                current_metric.average_value = current_metric.current_value / m.total_value



