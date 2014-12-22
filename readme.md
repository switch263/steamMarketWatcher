Steam Market Watcher
- - - - -  - - - - - 

Steam Market Watcher is a little Python script that allows you to check at constant intervals over items you're looking for in the Steam Community Market. It lets you enter a price, and whenever one of your items meets the set price, it alerts you.

Usage:

    python ./marketWatcher --help | [-f path | item_name price] [-e]

        --help : displays this message.
        -f : reads the input into the file at path.
             File syntax : "object_name" price [newline]
             Your file can have as many lines as you'd like.
        -e : allows you to enter a price in euros.
        
Example file syntax:

    "avon of the crescent moon" 0.15
    lucentyr 4.20
    "Andalmere the Litigon" 0.99
    
Using upper or lower-case letters will not change anything.

Feel free to contact me about anything, you can use this script any way you like, and modify it.
