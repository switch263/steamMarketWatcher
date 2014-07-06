import sys
import json
import urllib2
from time import sleep
from HTMLParser import HTMLParser

TIME_INTERVAL = 0
STEAM_QUERY_URL = ''
STEAM_QUERY_END = ''
STEAM_LISTING = ''

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
    print 'python ./marketWatcher --help | [-f path | item_name price] [-e]'
    print
    print '    --help : displays this message.'
    print '    -f : reads the input into the file at path.'
    print '    File syntax : "object_name" price [newline]'
    print '    Your file can have as many lines as you\'d like.'
    print '    -e : allows you to enter a price in euros.'
    exit()

# Turns our objects_list into a more useful one (and slightly bigger)
def formalize_names():
    global objects_list

    new_table = []

    for sub in objects_list:
        if not sub[1].replace('.', '', 1).isdigit():
            print "Second argument must be a price, thus a number. Wrong parameter:" + sub[1]
            exit()

        object_name = sub[0].lower()
        object_name_titled = object_name.title()
        object_name_titled = object_name_titled.replace(" Of ", " of ")
        object_name_titled = object_name_titled.replace(" The ", " the ")
        object_name_display = object_name_titled
        object_name_titled = object_name_titled.replace(' ', '%20')
        object_name = object_name.replace(' ', '%20')

        object_price = sub[1]

        new_table.append([object_name, object_name_titled, object_name_display, object_price])

    objects_list = new_table

# Herits from HTMLParser, because it's an HTML parser.
class LinkExtractor(HTMLParser):
    pricef = 999

    def reset(self):
        HTMLParser.reset(self)
        self.extracting = False
        self.links = []

    # Action at the beginning of a tag
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href' and value == STEAM_LISTING + objects_list[iterator][1]:
                    self.extracting = True

    # Action inside two tags
    def handle_data(self, data):
        global iterator
        if self.extracting:
            if data[-3:] == 'USD':
                pricef = float(data[:-4])
                if pricef < float(objects_list[iterator][3]) * EUROBOOL:
                    print objects_list[iterator][2] + ":"
                    if (EUROBOOL == 1):
                        print "Found a good price :", pricef, "USD", "\a"
                    else:
                        print "Found a good price :", pricef / EUROBOOL, "Euros", "\a"

                    if len(objects_list) == 1:
                        exit()
                    else:
                        objects_list.remove(objects_list[iterator])
                        iterator -= 1

    # Action at the end of a tag
    def handle_endtag(self, tag):
        if tag == 'a':
            self.extracting = False

# main function, sorry for the mess
if __name__ == '__main__':
    objects_list = [] # Contains every object the user inputed.
    EUROBOOL = 1 # Euro/Dollar modifier.

    readConfig() # Reads the configuration file and sets some constants.
        # You shouldn't really modify this file, by the way.

    # Basic command line arguments parsing.
    if '--help' in sys.argv:
        displayUsage()

    if '-f' in sys.argv:
        if (len(sys.argv) == 3) or (len(sys.argv) == 4 and '-e' in sys.argv):
            readFile(sys.argv[2])
        else:
            displayUsage()
    else:
        if (len(sys.argv) == 3) or (len(sys.argv) == 4 and '-e' in sys.argv):
            # Hack to check if true number.
            if not sys.argv[2].replace('.', '', 1).isdigit():
                print "Second argument must be a price, thus a number. Wrong parameter: " + sys.argv[2]
                exit()

            objects_list = [[sys.argv[1], sys.argv[2]]]
        else:
            displayUsage()

    if '-e' in sys.argv:
        EUROBOOL = 1.36

    # Turns the objects list into a more useful objects list.
    formalize_names()

    # One render per object, it's page-related.
    renders_list = []

    for sub in objects_list:
        page = urllib2.urlopen(STEAM_QUERY_URL + sub[0] + STEAM_QUERY_END).read()
        render = json.loads(page)
        renders_list.append(render)

    # Instantiates the HTML parser...
    le = LinkExtractor()

    # Big loop of doom.
    while True:
        iterator = 0
        for render in renders_list:
            le.feed(render['results_html'])
            iterator += 1
        sleep(TIME_INTERVAL)
