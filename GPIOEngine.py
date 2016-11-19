try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  You need superuser privileges.  You can achieve this by using 'sudo' to run your script")
from conf import *


class PowerMode:
    """Fake enum"""
    TWITTER, GLOW, OFF = range(3)


class GPIOEngine:
    """Handles GPIO button interrupts for user control"""

    def __init__(self):
        print("[!] Starting GPIO Handler...")
        self.powerMode = PowerMode.OFF  # Set to PowerMode.TWITTER if no button is hooked up
        self.firstTimeOn = True
        self.setupGPIO()

    def stop(self):
        GPIO.cleanup()

    def setupGPIO(self):
        """Set up RPi.GPIO Lib & register callbacks"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        GPIO.setup(POWER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(POWER_PIN, GPIO.FALLING, callback=self.updatePowerMode, bouncetime=200)

    ## ---- Power ------------------------------------------------------------------------------------------------------
    def updatePowerMode(self, channel):
        """Callback for Mode button. <channel> is needed as part of GPIO.add_event_detect callback spec"""
        if self.powerMode == PowerMode.OFF:
            self.powerMode = PowerMode.TWITTER
            self.firstTimeOn = True
            print("[!] Twitter Feed Mode Enabled")

        elif self.powerMode == PowerMode.TWITTER:
            self.powerMode = PowerMode.GLOW
            print("[!] Glow Mode Enabled")

        elif self.powerMode == PowerMode.GLOW:
            self.powerMode = PowerMode.OFF
            print("[!] Standby Mode Enabled")

    def wasOff(self):
        """Returns true if the On/Off toggle was just switched to On"""
        if self.firstTimeOn:
            self.firstTimeOn = False
            return True
        return False
