# PiXel (Pi Pixel)
Make NeoPixels react to Twitter trends

<img src="https://github.com/ianmclinden/PiXel/blob/master/img/TweetTree.png" width="240">

[Reacting to live tweets](https://github.com/ianmclinden/PiXel/blob/master/img/TweetTree_TwitterMode.mp4)

[Reacting to a special hashtag](https://github.com/ianmclinden/PiXel/blob/master/img/TweetTree_TwinkleWhite.mp4)

# Overview
- PiXel runs on a [Raspberry Pi](https://www.raspberrypi.org), and triggers LED animations based on current [Twitter](https://twitter.com/) trends.
- For every tweet in the last 5 seconds that matches one of the user supplied keywords, PiXel flashes a random LED on the strip.
- If nearly the same number of tweets as pixels are found, then a random special animation is triggered
- If barely any tweets are found, then the pixels glow dimly
- If a user supplied special keyword or author is found, then a specific special animation is triggered.
- A toggle button can be added to cycle the array between the Standby/OFF, Twitter, and Glow states

# Hardware Requirements
- [Raspberry Pi](https://www.raspberrypi.org) (2x/3x) with Latest Raspbian
- Raspberry Pi Power Supply (2+ Amps)
- WS281X LED Strip ([NeoPixel](https://www.adafruit.com/category/168) or clone)
- 5v Power Supply - (0.06 * Number of Pixels) Amps
- Logic Level Conversion (see [Adafruit Guide to Using NeoPixels with Raspberry Pi](https://learn.adafruit.com/neopixels-on-raspberry-pi/wiring) for more details on wiring)
- (Optional) Toggle button (for controlling modes)

Alternatively, Order and Assemble a [NeoPixel Shield](https://oshpark.com/shared_projects/EfBTUL7t)

<a href="https://oshpark.com/shared_projects/EfBTUL7t"><img src="https://oshpark.com/assets/badge-5b7ec47045b78aef6eb9d83b3bac6b1920de805e9a0c227658eac6e19a045b9c.png" alt="Order from OSH Park"></img></a>

# Dependencies
[RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO)
- Should be preinstalled in newer Raspbian

[rpi_ws281x](https://github.com/jgarff/rpi_ws281x)
- Follow library installation instructions

[Python Twitter](https://github.com/bear/python-twitter)
- Install with `$ pip install python-twitter` or follow the link and install manually.

# Setup
- Follow [Adafruit Guide to Using NeoPixels with Raspberry Pi](https://learn.adafruit.com/neopixels-on-raspberry-pi/wiring) to set up WS281X Strip. Connect to [GPIO18, GND]
- (Optional): Connect Toggle button to [GPIO24, GND] for Mode Toggle
- Install [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) & [Dependencies](#dependencies) on Raspberry Pi (see [raspbian installation guide](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) for more details)
- Set up Twitter Dev account and register for API keys. See [python-twitter docs](https://python-twitter.readthedocs.io/en/latest/) for information about setting up API Keys
- Configure conf.py with API keys, LED colors, and correct GPIO pins
- run main.py with super user permissions, i.e. `sudo python $PIXEL_PATH/PiXel/main.py` OR to run at startup (hack-y)
```
## Enable PiXel @ start
if ! ps ax | grep -v grep | grep python > /dev/null; then
        screen -d -m -S PiXel bash -c 'cd $PIXEL_PATH/PiXel/ && sudo python main.py'
fi
```

# Queries
PiXel uses 3 query types. For information about formatting, see [Twitter Search API documentation](https://www.google.com/search?q=twitter+search+API&ie=utf-8&oe=utf-8). All three queries are included in the `q` field of a Twitter Search call.
- QUERY_KEYWORDS: These keywords trigger a single flash.
- QUERY_SPECIALS: These keywords trigger a special animation.
- QUERY_FROM_USERS: If a tweet was written by this user a special animation is triggered.

# Author
Ian McLinden, 2016
