# -*- coding: utf-8 -*-

import sys
import json
import urllib2
from time import sleep
from HTMLParser import HTMLParser

import warnings
warnings.filterwarnings("ignore")

TIME_INTERVAL   = 0
STEAM_QUERY_URL = ''
STEAM_QUERY_END = ''
STEAM_LISTING   = ''
EUROBOOL        = 1
objects_list    = []
renders_list	= []
foundList	= []
iterator        = 0
found           = False
reverse		= False

# Reads configuration file and sets some CONSTANTS. Sorry for shouting.
def readConfig():
    f = open('.smwrc')
    lines = f.readlines()

    global TIME_INTERVAL
    global STEAM_QUERY_URL
    global STEAM_QUERY_END
    global STEAM_LISTING

    TIME_INTERVAL = int(lines[0].split('=', 1)[1])
    STEAM_QUERY_URL = lines[1].split('=', 1)[1][:-1]
    STEAM_QUERY_END = lines[2].split('=', 1)[1][:-1]
    STEAM_LISTING = lines[3].split('=', 1)[1][:-1]

    f.close()

# Reads a file and uses its content to fill objects_list. Used with '-f'
def readFile(path):
    global objects_list
    f = open(path)
    lines = f.readlines()

    for line in lines:
        objects_list.append([line[1:].split('"')[0], line[1:].split('"')[1][1:-1]])

    f.close()

# Displays the script's usage.
def displayUsage():
    print 'python ./marketWatcher --help | [-f path | item_name price] [-e] [-r]'
    print
    print '    --help : displays this message.'
    print '    -f : reads the input into the file at path.'
    print '    File syntax : "object_name" price [newline]'
    print '    Your file can have as many lines as you\'d like.'
    print '    -e : allows you to enter a price in euros.'
    print '    -r : allows you to perform the search in reverse, to check prices going up.'
    exit()

def capitalize(line):
    return ' '.join([s[0].upper() + s[1:] for s in line.split(' ')])

# Turns our objects_list into a more useful one (and slightly bigger)
def formalize_names():
    global objects_list
    new_table = []

    for sub in objects_list:
        if not sub[1].replace('.', '', 1).isdigit():
            print "Second argument must be a price, thus a number. Wrong parameter:" + sub[1]
            exit()

        object_name = sub[0]#.lower()
        object_name_titled = capitalize(object_name)
        object_name_titled = object_name_titled.replace(" Of ", " of ")
        object_name_titled = object_name_titled.replace(" The ", " the ")
        object_name_display = object_name_titled
        object_name_titled = object_name_titled.replace(' ', '%20')
        object_name_titled = object_name_titled.replace('(', '%28')
        object_name_titled = object_name_titled.replace(')', '%29')
        object_name_titled = object_name_titled.replace('™', '%E2%84%A2')
        object_name_titled = object_name_titled.replace('|', '%7C')
        object_name = object_name.replace(' ', '%20')
        object_name = object_name.replace('(', '%28')
        object_name = object_name.replace(')', '%29')
        object_name = object_name.replace('™', '%E2%84%A2')
        object_name = object_name.replace('|', '%7C')

        object_price = sub[1]

        new_table.append([object_name, object_name_titled, object_name_display, object_price])

    objects_list = new_table

class LinkExtractor(HTMLParser):
    pricef = 999

    def reset(self):
        HTMLParser.reset(self)
        self.extracting = False

    # Action at the beginning of a tag
    def handle_starttag(self, tag, attrs):
        if tag == 'a' and not found:
            for name, value in attrs:
		test = STEAM_LISTING + objects_list[iterator][1]
		value = value.split('/')
		if (len(value) > 5):
		    value.pop(5)
		value = '/'.join(value)
                if iterator in range(len(objects_list)) and name == 'href' \
		and value == test:
                    self.extracting = True

    # Action inside two tags
    def handle_data(self, data):
        global iterator, found, objects_list, renders_list

        if self.extracting and not found:
            if data[-3:] == 'USD':
	    	# Get rid of symbols in the price tag
	    	if (data[0] == '$'):
                    pricef = float(data[1:-4])
		else:
		    pricef = float(data[:-4])

		if not reverse:
		    if pricef < float(objects_list[iterator][3]) * EUROBOOL:
		        print "- " + objects_list[iterator][2] + ":"
		        if (EUROBOOL == 1):
			    print "================================================"
		    	    print "/!\\ FOUND A GOOD PRICE :", pricef, "USD /!\\\n", "\a"
			    print "================================================"
		        else:
			    print "================================================"
		    	    print "/!\\ FOUND A GOOD PRICE :", pricef / EUROBOOL, " Euros /!\\\n", "\a"
			    print "================================================"

		        if len(objects_list) == 1:
		    	    exit()
		        else:
		    	    self.extracting = False
		    	    found = True
		    else:
		        print "- " + objects_list[iterator][2] + ":"
		        if (EUROBOOL == 1):
		    	    print "Found a bad price: " + str(pricef) + "USD\n"
		        else:
		    	    print "Found a bad price: " + str(pricef / EUROBOOL) + " Euros\n"
		            self.extracting = False
		else:
		    if pricef > float(objects_list[iterator][3]) * EUROBOOL:
		        print "- " + objects_list[iterator][2] + ":"
		        if (EUROBOOL == 1):
			    print "================================================"
		    	    print "/!\\ HIGHER THAN SPECIFIED: ", pricef, "USD /!\\\n", "\a"
			    print "================================================"
		        else:
			    print "================================================"
		    	    print "/!\\ HIGHER THAN SPECIFIED: ", pricef / EUROBOOL, " Euros /!\\\n", "\a"
			    print "================================================"

		        if len(objects_list) == 1:
		    	    exit()
		        else:
		    	    self.extracting = False
		    	    found = True
		    else:
		        print "- " + objects_list[iterator][2] + ":"
		        if (EUROBOOL == 1):
		    	    print "Still lower than specified: " + str(pricef) + "USD\n"
		        else:
		    	    print "Still lower than specified: " + str(pricef / EUROBOOL) + " Euros\n"
		            self.extracting = False
		    

    # Action at the end of a tag
    def handle_endtag(self, tag):
        if tag == 'a' and found:
            self.extracting = False

# main function, sorry for the mess
def main():
    global objects_list, foundList, iterator, EUROBOOL, found, reverse

    readConfig() # Reads the configuration file and sets some constants.
        # You shouldn't really modify this file, by the way.
	# Except if nothing is working because steam changed some urls!
	# But in that case the script might need a major overhaul anyway.

    # Basic command line arguments parsing.
    if '--help' in sys.argv:
        displayUsage()

    if '-r' in sys.argv:
        reverse = True

    if '-f' in sys.argv:
        if (len(sys.argv) >= 3):
	    print "Trying to read specified config file: " + sys.argv[2] + "..."
            readFile(sys.argv[2])
	    print "Success!"
        else:
            displayUsage()
    else:
        if (len(sys.argv) >= 3):
            # Hack to check if true number.
            if not sys.argv[2].replace('.', '', 1).isdigit():
                print "Second argument must be a price, thus a number. Wrong parameter: " + sys.argv[2]
		displayUsage()

            objects_list = [[sys.argv[1], sys.argv[2]]]
        else:
            displayUsage()

    if '-e' in sys.argv: # Update me from time to time! :> Could get it from web but lazy
        EUROBOOL = 1.11

    print "/!\ DISCLAIMER: Know that the number of requests you can send to the steam\n\
market is limited. At some point, you will get a 429 HTTP error, which\n\
means that Steam won't answer you anymore. I don't know how long it takes\n\
for Steam to allow requests for you again. This is why the default timestep\n\
is 2 minutes : so that you don't get timed out too quickly.\n"

    # Turns the objects list into a more useful objects list.
    formalize_names()

    for sub in objects_list:
        page = urllib2.urlopen(STEAM_QUERY_URL + sub[0] + STEAM_QUERY_END).read()
        render = json.loads(page)
        renders_list.append(render)

    for render in renders_list:
        foundList.append(False)

    # Instantiates the HTML parser...
    le = LinkExtractor()

    # Main loop
    while True:
    	for i in range(len(objects_list)):
	    foundList[i] = False
        iterator = 0

	for render in renders_list:
	    found = False
	    le.feed(render['results_html'])
	    if found and iterator in range(len(foundList)):
	    	foundList[iterator] = True
	    iterator = iterator + 1

	# Remove found items.
	mod = 0
	for i in range(len(foundList)):
	    if foundList[i]:
	        renders_list.pop(i - mod)
		objects_list.pop(i - mod)
		mod += 1
	foundList = [v for v in foundList if not v]

        if len(objects_list) == 0:
	    print "==== Succesfully found all the items! :) ===="
            exit()

	print "\nScript is going to keep looking for :"
	for e in objects_list:
	    print "\t* " + e[2]
	
	print
	for s in range(TIME_INTERVAL):
	    sys.stdout.write("\rSleeping for " + str(TIME_INTERVAL - s) + " seconds...")
	    sleep(1)
        #sleep(TIME_INTERVAL)

main()
