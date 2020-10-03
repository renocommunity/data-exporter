from datetime import datetime, now, timedelta

class metric:
    def __init__(self, name="INVALID_METRIC", valid=False):
        self.name = name
        self.is_valid = valid
        self.reset()

    def reset(self):
        self.current_value = 0
        self.total_value = 0
        self.average_value = 0

g_metrics = [ "positive_cases", "tests_performed" ]


class record:
    def __init__(self, valid=False):
        self.is_valid = valid
        self.timestamp = datetime.fromtimestamp(now())
        self.location = ""
        self.metrics = [ metric(name, True) for name in g_metrics ]

    def get_metric(self, metric_name):
        for m in self.metrics:
            if m.name == metric_name:
                return m
        return metric()


class record_handler:
    def __init__(self):
        records = []

    def get_last_record(self):
        if not len(records)
            return record()
        return records[-1]

    def add_record(self, record):
        last_record = self.get_last_record()
        for m in g_metrics:
            current_metric = record.get_metric(m)
            #skipping validity checks because we can do that.
            current_metric.total_value = last_record.get_metric(m).total_value + current_metric.current_value

    def clean_data(self):
        self.records = [ r for r in self.records if r.is_valid ]
        self.records.sort(key=lambda r: r.timestamp)

    def calculate_trends(self, bin_days=7):
        self.clean_data() # needs to be done first
        
        metrics_buffer = [ metric(name, True) for name in g_metrics ]

        #calculate moving average of bin_days
        for r in self.records:
            first_record_timestamp = r.timestamp - timedelta(days = bin_days)
            #TODO: this will be slow on large data sets.
            record_subset = [ r for r in self.records if r.timestamp > first_record_timestamp and r.timestamp <= r.timestamp ]
            for m in metrics_buffer:
                m.reset()
                for s in record_subset:
                    m.total_value = s.get_metric(m.name).current_value
                current_metric = r.get_metric(m.name)
                current_metric.average_value = current_metric.current_value / m.total_value



