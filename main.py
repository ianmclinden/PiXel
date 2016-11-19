"""
PiXel - Twitter driven NeoPixels
--------------------------------
Author : Ian McLinden
Date: 10/29/16

Description: PiPixel Drives NeoPixels based on activity on Twitter.

Optional GPIO Button to cycle between Off, Twitter Feed Mode, and Glowing

"""

from TwitterEngine import *
from NeoPixelEngine import *
from GPIOEngine import *
import time


def main():
    # Print Main screen
    print(GUI_STR)

    gpioEngine = GPIOEngine()
    neoPixelEngine = NeoPixelEngine()
    twitterEngine = TwitterEngine()

    while True:
        try:
            if gpioEngine.powerMode == PowerMode.GLOW:
                neoPixelEngine.randomColorGlow(25)
                time.sleep(POLL_FREQUENCY)

            elif gpioEngine.powerMode == PowerMode.TWITTER:
                if gpioEngine.wasOff():
                    neoPixelEngine.pickRandomSpecialAnimation()
                    time.sleep(POLL_FREQUENCY)
                    continue

                new_tweets, new_specials = twitterEngine.getNewMatches()

                if PRINT_NEW_TWEETS and (new_tweets > 0):
                    print("[+] %d New Tweets" % new_tweets)
                if PRINT_NEW_TWEETS and (new_specials > 0):
                    print("[+] %d New Special Tweets" % new_specials)

                neoPixelEngine.animate(new_tweets, new_specials)
                time.sleep(POLL_FREQUENCY)

        except (KeyboardInterrupt, SystemExit):
            print("\n\n[*] Exiting ...")
            neoPixelEngine.stop()
            gpioEngine.stop()
            exit(0)

if __name__ == "__main__":
    main()
