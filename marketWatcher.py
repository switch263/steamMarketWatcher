import sys
import json
import urllib2
from time import sleep
from HTMLParser import HTMLParser

class LinkExtractor(HTMLParser):

    pricef = 999

    def reset(self):
        HTMLParser.reset(self)
        self.extracting = False
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href' and value == 'http://steamcommunity.com/market/listings/570/' + object_name.title():
                    self.extracting = True

    def handle_data(self, data):
        if self.extracting:
            if data[-3:] == 'USD':
                pricef = float(data[:-4])
                if pricef < price:
                    print display_name + ":"
                    print "Found a good price ! ->", pricef / 1.36, "\a"
                    exit()

    def handle_endtag(self, tag):
        if tag == 'a':
            self.extracting = False

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '--help' or len(sys.argv) > 4:
        print "Usage:"
        print "    python marketWatcher.py object_name price [-e]"
        print "Options:"
        print "    -e      Allows you to type the price in euros."
        exit()

    b = True

    object_name = sys.argv[1]
    object_name = object_name.replace(' ', '%20').lower()
    object_name_titled = object_name.title()
    object_name_titled = object_name_titled.replace("%20Of%20", "%20of%20")
    object_name_titled = object_name_titled.replace("%20The%20", "%20the%20")

    display_name = object_name_titled.replace('%20', ' ')

    if len(sys.argv) == 4 and sys.argv[3] == '-e':
        price = float(sys.argv[2]) * 1.36
    else:
        price = float(sys.argv[2])

    page = urllib2.urlopen("http://steamcommunity.com/market/search/render/?query=" + object_name + "&start=0&count=10").read()
    render = json.loads(page)
    le = LinkExtractor()
    while True:
        if b:
            le.feed(render['results_html'])
            b = False
        else:
            sleep(2)
            b = True
