from ..models import Metric, Record

class RecordHandler:
    def __init__(self, metric_names_to_create = []):
        self.records = []
        self.metrics_buffer = [ Metric(name, True) for name in metric_names_to_create ]

    #Create a record with metrics matching those in *this
    def create_record(self):
        ret = Record()
        ret.validate()
        ret.create_metrics([m.name for m in self.metrics_buffer])
        return ret

    def get_last_record(self):
        return records[-1] if records else Record()

    #Add a record to *this
    def add_record(self, record):
        if not record.do_metrics_contain(self.metrics_buffer):
            raise ValueError("Data shape mismatch")

        last_record = self.get_last_record()
        for m in metrics_buffer:
            current_metric = record.get_metric(m.name)
            #skipping validity checks because we can do that.
            current_metric.total_value = last_record.get_metric(m.name).total_value + current_metric.current_value
        self.records.append(record)

    def save_records(self):
        for r in self.records:
            r.save()

    def print_records(self):
        for i,r in enumerate(self.records):
            print("Record {i}")
            print("Timestamp: {r.timestamp}")
            print("Location: {r.location}")
            for m in r.metrics:
                print("Metric {m.name}")
                print("  current value: {m.current_value}")
                print("  total value: {m.total_value}")
                print("  average value: {m.average_value}")

    def clean_data(self):
        self.records = [ r for r in self.records if r.is_valid ]
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



