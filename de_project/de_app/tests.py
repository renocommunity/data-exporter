from django.test import TestCase
from pprint import pprint
from .models import Metric, Record, RecordHandler
from django.core import serializers
from django.test import Client
import logging

logger = logging.getLogger(__name__)

class RecordStorageTestCase(TestCase):

    def setUp(self):
        self.test_metric_names = ["test_metric", "another_test_metric"]
        self.metric_values = [ 3, 44, 100 ]
        self.handler = RecordHandler(name="test_record_handler", metric_names=self.test_metric_names)
        self.handler.initialize()
        self.client = Client()

    def are_records_stored_successfully(self):
        all_records = Record.objects.all()

        logger.debug(self.handler.get_records_as_json())

        return len(all_records) > 0 #TODO: check data

    def storing_records_test(self):
        logger.info("Test: storing_records_test")

        #Make sure we aren't using stale data
        logger.debug("Pre-test data")
        self.assertFalse(self.are_records_stored_successfully())

        #Create a test record. This may or may not be stored.
        test_record = self.handler.create_record()
        
        #Make sure our test metrics were created and add values to them
        for i,n in enumerate(self.test_metric_names):
            test_record.set_metric_value(n, "current_value", self.metric_values[0])
            test_record.set_metric_value(n, "total_value", self.metric_values[1])
            test_record.set_metric_value(n, "average_value", self.metric_values[2])

        self.handler.add_record(test_record)

        #Just make sure this doesn't auto-fail. We don't care if it works here.
        #NOTE: THIS MAY CLOBBER VALUES SET ABOVE
        self.handler.calculate_trends()

        #Write our test data to the database
        self.handler.save_records()

        #Check if we successfully stored data
        logger.debug("Post-test data")
        self.assertTrue(self.are_records_stored_successfully())

    def get_records_test(self):
        logger.info("Test: get_records_test")

        response = self.client.get('/test_record_handler/data-file.json')
        self.assertEqual(response.status_code, 200)
        logger.debug(response.content)

    def get_invalid_records_test(self):
        logger.info("Test: get_records_test")

        response = self.client.get('/invalid_record_handler/data-file.json')
        self.assertEqual(response.status_code, 404)

    def test_all_in_order(self):
        self.storing_records_test()
        self.get_invalid_records_test()
        self.get_records_test()
