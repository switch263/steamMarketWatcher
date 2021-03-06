Steam Market Watcher
- - - - -  - - - - - 

#Introduction

Steam Market Watcher is a little Python script that allows you to check at constant intervals over items you're looking for in the Steam Community Market. It lets you enter a price, and whenever one of your items meets the set price, it alerts you.

#Required

* [Python 2.7](https://www.python.org/download/releases/2.7/)

#How do I use this on windows?

Download the requirement above, install it.

Download the git repository (this project, « Clone or download » green button, top right corner), go into the corresponding folder, press shift + right click -> Open command window here.

If this option isn't available for some reason, press Win+R, type `cmd`, then navigate to the folder. Example if you want to go to D:\Documents\steamMarketWatcher : http://i.imgur.com/9moUMbP.png

Then you can use the script as specified in the usage below.

#Usage:

    python ./marketWatcher --help | [-f path | item_name price] [-e] [-r]

        --help : displays this message.
        -f : reads the input into the file at path.
             File syntax : "object_name" price [newline]
             Your file can have as many lines as you'd like.
        -e : allows you to enter a price in euros.
        -r : allows you to perform the search in reverse, to check prices going up.
        
Example file syntax:

    "avon of the crescent moon" 0.15
    lucentyr 4.20
    "Andalmere the Litigon" 0.99
    "StatTrak™ M4A1-S | Blood Tiger (Minimal Wear)" 200
    
Using upper or lower-case letters will not change anything.

By default the script updates once every 60 seconds. You can change this in the .smwrc file, by changing the value after `time_interval=`. Don't go too low because the steam market has a limit on the number of requests you can do. Too much requests, and you'll get a timeout (HTTP error 429). I wouldn't advise going below 15 seconds.

Feel free to contact me about anything, you can use this script any way you like, and modify it.

#In case of any issue

Open an issue on github or shoot me an email at baruss.thomas@gmail.com

Hope this script serves you well!

#Possible issues

* Unicode characters that I don't handle. This will probably happen so tell me asap, should be a quick fix.
* Steam changing the market's structure. Since the crawling is based on hard-coded URLs, this could be broken in an instant if Steam decides to update their URLs.

If the item isn't found, make the search yourself on https://steamcommunity.com/market/ and look if
you didn't mistype something or if the item's associated url is a bit funky. Then tell me if you can't
fix it yourself. 
