from django.test import TestCase
from pprint import pprint
from .models import Metric, Record
from .data_handling.RecordHandler import RecordHandler

class RecordStorageTestCase(TestCase):

    def setUp(self):
        self.test_metric_names = ["test_metric"]
        self.metric_values = [ 3, 4, 3 ]
        self.handler = RecordHandler(self.test_metric_names)
        pass

    def areRecordsStoredSuccessfully(self):
        all_records = Record.objects.all()
        # print("---- All records ----")
        # pprint(vars(all_records))

        # all_metrics = Metric.objects.all()
        # print("---- All metrics ----")
        # pprint(vars(all_metrics))

        return len(all_records) > 0 #TODO: check data

    def test_storing_records(self):
        #Make sure we aren't using stale data
        self.handler.print_records()
        self.assertFalse(self.areRecordsStoredSuccessfully())

        #Create a test record. This may or may not be stored.
        test_record = self.handler.create_record()
        
        #Make sure our test metrics were created and add values to them
        for n in self.test_metric_names:
            metric = test_record.get_metric(n)
            # self.assertTrue(metric.is_valid)
            metric.current_value = self.metric_values[0]
            metric.total_value = self.metric_values[1]
            metric.average_value = self.metric_values[2]

        #Write our test data to the database
        self.handler.save_records()

        #Check if we successfully stored data
        self.handler.print_records()
        self.assertTrue(self.areRecordsStoredSuccessfully())