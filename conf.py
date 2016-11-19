## ==== CONFIGURABLES ==================================================================================================
PRINT_NEW_TWEETS = True  # Print the number of new tweets to the Terminal

## ---- LED Hardware ---------------------------------------------------------------------------------------------------
LED_COUNT       = 50      # Number of LED pixels.
LED_FADE_STEP   = 32      # How many steps of Fade In / Fade Out
LED_UPDATE_FREQ = 32      # Hz - How often to send LED states to NeoPixel
THREAD_OHD_TIME = 0.002   # Thread overhead time estimate
# Below - For NeoPixel Lib
LED_FREQ_HZ     = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA         = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS  = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False   # True to invert the signal (when using NPN transistor level shift)

SUCCESS_COLORS = [(255, 0, 0), (0, 200, 0), (0, 0, 255)]  # List of Colors RGB

# ---- GPIO Hardware ---------------------------------------------------------------------------------------------------
LED_PIN         = 18      # GPIO pin connected to the pixels (must support PWM!).
POWER_PIN       = 24      # GPIO pin connected to enable / disable button

## ---- Twitter --------------------------------------------------------------------------------------------------------
POLL_FREQUENCY = 5  # Poll API every POLL_FREQUENCY Seconds, min 5
QUERY_KEYWORDS = ["arduino", "raspberrypi", "neopixel"]  # OR'd Together
QUERY_SPECIALS = ["special"]  # Trigger special animation
QUERY_FROM_USERS = []

# Need to set up app on dev.twitter.com for API Keys
CONSUMER_KEY = "XXXXXXXXXXXXXXXXX"
CONSUMER_SECRET = "XXXXXXXXXXXXXXXXX"
ACCESS_TOKEN_KEY = "XXXXXXXXXXXXXXXXX"
ACCESS_TOKEN_SECRET="XXXXXXXXXXXXXXXXX"


# ---- GUI -------------------------------------------------------------------------------------------------------------
GUI_STR  ="############################################################\n"  # Printed at the beginning
GUI_STR +="#    PiXel  -  Make NeoPixels react to Twitter trends      #\n"
GUI_STR +="############################################################\n"
GUI_STR +="Press Ctl+C to Exit ...\n\n"