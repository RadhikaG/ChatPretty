# ChatPrintr
A pretty-printer for (for now) WhatsApp chats.

Hi. This is a little script for pretty-printing long WhatsApp conversations you'd like to send to someone, like stitching together multiple screenshots of the coversation.
**This is still a work in progress.**
This was inspired by the default ugly WhatsApp message copypasta and the cumbersome process of taking multiple screenshots for a single conversation.

This works only on Python2.7, since I plan on porting it to Flask, which too only supports Python2.7 currently.

**About the files:**
* `timeName.py`: The actual Python script
* `timeName.sh`: For testing regexes
* `chat.txt`: A WhatsApp copypasta for testing

# To-do List
* Stitch together the message snippets
* Add the timestamps
* Make the web app
* Make it graphically more accurate to the WhatsApp UI
