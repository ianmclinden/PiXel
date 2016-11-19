import time
import random
import threading
from neopixel import *
from conf import *


def getRandomColor(colorsList):
    """Returns a random color from <colorsList> or OFF"""
    if len(colorsList) > 0:
        return colorsList[random.randint(0, len(colorsList)-1)]
    return 0, 0, 0


def getDimmedRGB(color, alpha=255):
    """Returns dimmed RGB values, with low and high pass to ensure LEDs are fully off or on"""
    if alpha >= 253:  # int is 1
        return color
    elif alpha <= 2:  # int is 0
        return 0, 0, 0
    else:
        p = alpha/255.0
        r, g, b = color
        return int(r*p), int(g*p), int(b*p)


class NeoPixelEngine:
    """Pushes animations to hardware NeoPixel array based on the number of tweets & special tweets found"""

    def __init__(self):
        print("[!] Starting NeoPixel Engine ...")
        random.seed(time.time())
        # Set up Neopixel Strip
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.strip.begin()
        # start refresh Thread
        self.refresh = threading.Thread(target=self.refreshStrip, args=(1.0/LED_UPDATE_FREQ,))
        self.refresh.setDaemon(True)
        self.isAlive = True
        self.refresh.start()

    def stop(self):
        self.isAlive = False
        self.refresh.join()

    def animate(self, tweets, specials):
        """Wrapper for Animate thread handler"""
        random.seed(time.time())
        threading.Thread(target=self.animateThread, args=(tweets, specials,)).start()

    def animateThread(self, tweets, specials):
        """Chooses how to animate the hardware array, based on the number of tweets and special tweets"""
        if specials > 0:
            # Special tweet found
            self.whiteTwinkle()
        elif tweets >= 0:
            if (float(tweets)/LED_COUNT) > 0.9:
                # Almost saturated
                self.pickRandomSpecialAnimation()
            elif (float(tweets)/LED_COUNT) < 0.1:
                # Hardly any
                self.pickRandomGlow()
            else:
                # Moderate amount
                self.flashRandom(tweets)

    ## ---- Animations -------------------------------------------------------------------------------------------------
    def pickRandomSpecialAnimation(self):
        random.seed(time.time())
        random.choice([
            self.solidColorWipe,
            self.randomColorWipe,
            self.solidColorTwinkle,
            self.randomColorTwinkle,
            self.solidColorLadder,
            self.randomColorLadder,
            self.candyCane
        ])()

    def pickRandomGlow(self):
        random.seed(time.time())
        random.choice([
            self.solidColorGlow,
            self.randomColorGlow
        ])(15)

    def showcaseAnimations(self):
        """Runs through all the animations in the class, for test & showcase"""
        self.flashRandom(LED_COUNT)
        self.solidColorWipe()
        time.sleep(POLL_FREQUENCY/2)
        self.randomColorWipe()
        time.sleep(POLL_FREQUENCY/2)
        self.solidColorTwinkle()
        self.whiteTwinkle()
        self.randomColorTwinkle()
        self.solidColorGlow(25)
        time.sleep(POLL_FREQUENCY)
        self.randomColorGlow(25)
        time.sleep(POLL_FREQUENCY)
        self.solidColorLadder()
        self.randomColorLadder()
        self.candyCane()
        time.sleep(POLL_FREQUENCY/2)

    def flashRandom(self, number):
        """Flashes <number> random pixels a random color from SUCCESS_COLORS"""
        wait_s = float(POLL_FREQUENCY) / number
        hold = min(wait_s, 1.0)
        addrs = random.sample(range(0, LED_COUNT), number)
        for i in range(0, number):
            if (((i+1)*hold)+0.5) <= POLL_FREQUENCY:  # SO led don't overextend
                self.flash([addrs[i]], getRandomColor(SUCCESS_COLORS), hold=hold)
            time.sleep(wait_s)

    def solidColorWipe(self):
        """Wipes the same random color from SUCCESS_COLORS up the array"""
        color = getRandomColor(SUCCESS_COLORS)
        wait_s = float(POLL_FREQUENCY / (LED_COUNT * 2.0))
        hold = (POLL_FREQUENCY * 0.5)
        for i in range(0, LED_COUNT):
            self.flash([i], color, fade_in=(0.2*hold), hold=(0.6*hold), fade_out=(0.2*hold))
            time.sleep(wait_s)

    def randomColorWipe(self):
        """Wipes random colors from SUCCESS_COLORS up the array"""
        wait_s = float(POLL_FREQUENCY / (LED_COUNT * 2.0))
        hold = float(POLL_FREQUENCY * 0.5)
        for i in range(0, LED_COUNT):
            self.flash([i], getRandomColor(SUCCESS_COLORS), fade_in=(0.2*hold), hold=(0.6*hold), fade_out=(0.2*hold))
            time.sleep(wait_s)

    def solidColorTwinkle(self):
        """Twinkles the whole strip, all the same random color from SUCCESS_COLORS"""
        color = getRandomColor(SUCCESS_COLORS)
        wait_s = float(POLL_FREQUENCY) / LED_COUNT
        hold = min(wait_s, 1.0)
        addrs = random.sample(range(0, LED_COUNT), LED_COUNT) * 4
        for i in range(0, LED_COUNT):
            if (((i+1)*hold)+0.5) <= POLL_FREQUENCY:  # SO led don't overextend
                self.flash(addrs[(4 * i):(4 * i) + 4], color, hold=hold)
            time.sleep(wait_s)

    def whiteTwinkle(self):
        """Twinkles the whole strip white"""
        wait_s = float(POLL_FREQUENCY) / LED_COUNT
        hold = min(wait_s, 1.0)
        addrs = random.sample(range(0, LED_COUNT), LED_COUNT) * 4
        for i in range(0, LED_COUNT):
            if (((i+1)*hold)+0.5) <= POLL_FREQUENCY:  # SO led don't overextend
                self.flash(addrs[(4 * i):(4 * i) + 4], (255, 255, 255), hold=hold)
            time.sleep(wait_s)

    def randomColorTwinkle(self):
        """Twinkles the whole strip, each pixel a random color from SUCCESS_COLORS"""
        wait_s = float(POLL_FREQUENCY) / LED_COUNT
        hold = min(wait_s, 1.0)
        addrs = random.sample(range(0, LED_COUNT), LED_COUNT) * 4
        for i in range(0, LED_COUNT):
            if (((i+1)*hold)+0.5) <= POLL_FREQUENCY:  # SO led don't overextend
                self.flash(addrs[(4 * i):(4 * i) + 4], getRandomColor(SUCCESS_COLORS), hold=hold)
            time.sleep(wait_s)

    def solidColorGlow(self, intensity):
        """Turns whole strip on at <intensity> brightness, all the same random color from SUCCESS_COLORS"""
        color = getDimmedRGB(getRandomColor(SUCCESS_COLORS), intensity)
        self.flash(range(0,LED_COUNT), color, fade_in=(0.2*POLL_FREQUENCY), hold=(0.6*POLL_FREQUENCY), fade_out=(0.2*POLL_FREQUENCY))

    def randomColorGlow(self, intensity):
        """Turns whole strip on at <intensity> brightness, each pixel a random color from SUCCESS_COLORS"""
        for led in range(0, LED_COUNT):
            color = getDimmedRGB(getRandomColor(SUCCESS_COLORS), intensity)
            self.flash([led], color, fade_in=(0.2*POLL_FREQUENCY), hold=(0.6*POLL_FREQUENCY), fade_out=(0.2*POLL_FREQUENCY))

    def solidColorLadder(self):
        """Flashes a random color from SUCCESS_COLORS up the array, stepping up regular intervals"""
        color = getRandomColor(SUCCESS_COLORS)
        ledList = [l for l in range(0, LED_COUNT-int(POLL_FREQUENCY)+1) if (l % int(POLL_FREQUENCY) == 0)]
        for i in range(0, int(POLL_FREQUENCY)):
            for addr in ledList:
                self.flash([addr+i], color, hold=0.5)
            time.sleep(1)

    def randomColorLadder(self):
        """Flashes random colors from SUCCESS_COLORS up the array, stepping up regular intervals"""
        ledList = [l for l in range(0, LED_COUNT-int(POLL_FREQUENCY)+1) if (l % int(POLL_FREQUENCY) == 0)]
        for i in range(0, int(POLL_FREQUENCY)):
            for addr in ledList:
                self.flash([addr+i], getRandomColor(SUCCESS_COLORS), hold=0.5)
            time.sleep(1)

    def candyCane(self):
        """Pushes red and white stripes up the array"""
        color_div = int(LED_COUNT / 5)
        color = (255, 0, 0)
        wait_s = float(POLL_FREQUENCY / (LED_COUNT * 2.0))
        hold = float(POLL_FREQUENCY * 0.5)
        for i in range(0, LED_COUNT):
            if (i % color_div) == 0:
                if color == (255, 0, 0):
                    color = (255, 255, 255)
                else:
                    color = (255, 0, 0)
            self.flash([i], color, fade_in=(0.2*hold), hold=(0.6*hold), fade_out=(0.2*hold))
            time.sleep(wait_s)


    ## ---- Pixel Threads ----------------------------------------------------------------------------------------------
    def flash(self, addrs, color, fade_in=0.25, hold=0.0, fade_out=0.25):
        """Wrapper for Flash thread handler"""
        threading.Thread(target=self.flashThread, args=(addrs, color, fade_in, hold, fade_out,)).start()

    def flashThread(self, addrs, color, fade_in=0.25, hold=0.0, fade_out=0.25):
        """Flashes all pixels in <addrs> with <color>, run as a thread"""
        # fade in period
        wait_s = (fade_in / LED_FADE_STEP)
        alpha_mult = (255.0 / LED_FADE_STEP)
        for i in range(0, LED_FADE_STEP):
            for pixel in addrs:
                c = getDimmedRGB(color, alpha=((i+1)*alpha_mult))
                self.strip.setPixelColorRGB(pixel, *c)
            time.sleep(wait_s)

        if hold > 0:
            time.sleep(hold)

        # fade out period
        wait_s = (fade_out / LED_FADE_STEP)
        for i in range(LED_FADE_STEP, 0, -1):
            for pixel in addrs:
                c = getDimmedRGB(color, alpha=((i-1)*alpha_mult))
                self.strip.setPixelColorRGB(pixel, *c)
            time.sleep(wait_s)

    def refreshStrip(self, update_sleep):
        """LED_UPDATE_FREQ times per second the colors are sent to the NeoPixel Hardware Array"""
        while self.isAlive:
            self.strip.show()
            time.sleep(update_sleep)

        # Make sure to turn them off at the end
        for i in range(0, LED_COUNT):
            self.strip.setPixelColorRGB(i, 0, 0, 0)
        self.strip.show()
