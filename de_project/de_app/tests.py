from django.test import TestCase
from pprint import pprint
from .models import Metric, Record
from .data_handling.RecordHandler import RecordHandler
from django.core import serializers

class RecordStorageTestCase(TestCase):

    def setUp(self):
        self.test_metric_names = ["test_metric"]
        self.metric_values = [ 3, 4, 3 ]
        self.handler = RecordHandler(self.test_metric_names)
        pass

    def areRecordsStoredSuccessfully(self):
        all_records = Record.objects.all()
        
        print(self.handler.get_records_as_json())
        # print(serializers.serialize("json", all_records))

        return len(all_records) > 0 #TODO: check data

    def test_storing_records(self):
        #Make sure we aren't using stale data
        self.assertFalse(self.areRecordsStoredSuccessfully())

        #Create a test record. This may or may not be stored.
        test_record = self.handler.create_record()
        # print("TestRecord metrics: " + serializers.serialize('json', test_record.metrics.all()))
        
        #Make sure our test metrics were created and add values to them
        for i,n in enumerate(self.test_metric_names):
            metric = test_record.get_metric(n)
            # print("metric {i}: " + serializers.serialize('json', [metric,]))
            # self.assertTrue(metric.is_valid)
            metric.current_value = self.metric_values[0]
            metric.total_value = self.metric_values[1]
            metric.average_value = self.metric_values[2]

        self.handler.add_record(test_record)

        #Write our test data to the database
        self.handler.save_records()

        #Check if we successfully stored data
        self.assertTrue(self.areRecordsStoredSuccessfully())