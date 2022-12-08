import RPi.GPIO as GPIO
from time import sleep
SHUTTER = 24
HILIGHT = 23
IS_RECORDING = False
READY_FOR_HILIGHT = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(SHUTTER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(HILIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
print("Starting program")
try:
    while True:
        if GPIO.input(SHUTTER):
            if IS_RECORDING:
                print("Recording in progress")
                if GPIO.input(HILIGHT):
                    if READY_FOR_HILIGHT:
                        print("send hilight event")
                        READY_FOR_HILIGHT = False
                else:
                    READY_FOR_HILIGHT = True
            else:
                print("send start recording")
                IS_RECORDING = True
        else:
            if IS_RECORDING:
                print("send stop recording")
                IS_RECORDING = False
                READY_FOR_HILIGHT = True
            
        sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()