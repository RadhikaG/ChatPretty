# ChatPretty
A pretty-printer for (for now) WhatsApp chats.

**This is still a work in progress.**

Hi. This is a little script for pretty-printing long WhatsApp conversations you'd like to send to someone, like stitching together multiple screenshots of the coversation.

This was inspired by the default ugly WhatsApp message copypasta and the cumbersome process of taking multiple screenshots for a single conversation.

This works only on Python2.7, since I plan on porting it to Flask, which too only supports Python2.7 currently.

**About the files:**
* `imageGen.py`: The actual image generation script
* `server.py`: The Flask app which uses `imageGen.py`

# To-do List
* Make it fully-compatible with group chats
* Make it graphically more accurate to the WhatsApp UI

# Instructions

This is just for the basic testing environment, not for deployment.

* First create a virtualenv called my_env (or whatever you like). Make sure it uses Python2.7 and not Python3: `virtualenv -p /usr/bin/python2.7 my_env`
* Activate your virtualenv, then run: `pip install flask` and `pip install Pillow`
* Oh and of course: `git clone https://github.com/RadhikaG/ChatPretty.git`.
