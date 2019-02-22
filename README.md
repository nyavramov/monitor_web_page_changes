## Motivation

Web pages change all the time, so why not use some python to monitor web pages you're interested in for free? 

## What is this?

It's a python program that monitors a web page and e-mails you when a change on that page is detected.

## How does it work?

It uses selenium to open a web page, screen shot it, and then screenshot it again later to check for changes. This happens repeatedly. Changes are detected using perceptual hash differences between two screenshots (the old screenshot and the new screenshot). 


## Why perceptual hashes?

I initially thought that scraping the DOM might be a good way to look for changes, but it's just too much work writing a new DOM scraper every time you want to monitor a new site.  

## How do I use it?

First, make a virtualenv and install the dependencies by running the following 3 commands:

`virtualenv venv`

`source venv/bin/activate`

`python3 -m pip install -r requirements.txt`

Then fill out the e-mail (do NOT use your main e-mail, use a dummy account for safety!), password, and url you want to monitor in the main function. Also, I've included the binaries for chromedriver but feel free to download the new ones at [the official chromedriver website.](http://chromedriver.chromium.org/)

Finally, run `python3 monitor.py` to start monitoring a website.
