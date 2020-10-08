from bs4 import BeautifulSoup as BS
from ..models import RecordHandler, Record, Metric
import requests


####                   THIS IS EXAMPLE ONLY
##
## UNR changed their webpage, so this won't work
##
####

class UNRCovidScraper:
    def __init__(self):
        self.record_handler = RecordHandler.objects.get(name="UNRCovid")
        self.url = 'https://www.unr.edu/coronavirus/cases'

    def scrape(self):
        page = requests.get(self.url)
        page_content = BS(page.content, 'html.parser')
        results = page_content.find_all('p','large-body-copy')
        for i in reversed(range(len(results))):
            #Get a record to populate
            new_record = self.record_handler.create_record()
            
            #Scrape the data
            date = results[i].text.strip() #TODO: Make a date
            ul = results[i].find_next('ul')
            pos_text = ul.find_all('li') 
            pos_num = len(ul.find_all('li'))
            
            #Set the record values
            new_record.timestamp = date
            new_record.set_metric_value("positive_cases", "current_value", pos_num)

            #Add the record to our handler
            self.record_handler.add_record(new_record)
