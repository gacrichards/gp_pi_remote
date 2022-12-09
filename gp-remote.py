import RPi.GPIO as GPIO
import sys
from open_gopro import GoPro, Params
from time import sleep
LED_PIN = 25
SHUTTER_PIN = 24
HILIGHT_PIN = 23
is_encoding = False
READY_FOR_HILIGHT = True

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SHUTTER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(HILIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LED_PIN, GPIO.OUT)

def start_recording():
    gopro.ble_command.set_shutter(Params.Toggle.ENABLE)

def stop_recording():
    gopro.ble_command.set_shutter(Params.Toggle.DISABLE)

def tag_hilight():
    gopro.ble_command.tag_hilight()

def connect_gopro():
    global gopro
    gopro = GoPro(enable_wifi = False)
    gopro.open()

def init_gopro_settings():
    if gopro.is_encoding:
        stop_recording()
    gopro.ble_setting.video_performance_mode.set(Params.PerformanceMode.MAX_PERFORMANCE)
    gopro.ble_setting.max_lens_mode.set(Params.MaxLensMode.DEFAULT)
    gopro.ble_setting.camera_ux_mode.set(Params.CameraUxMode.PRO)
    gopro.ble_command.set_turbo_mode(False)
    assert gopro.ble_command.load_preset_group(Params.PresetGroup.VIDEO).is_ok

def blink_led():
    GPIO.output(LED_PIN, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(LED_PIN, GPIO.LOW)
    sleep(0.1)
    GPIO.output(LED_PIN, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(LED_PIN, GPIO.LOW)
    sleep(0.1)
    GPIO.output(LED_PIN, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(LED_PIN, GPIO.LOW)

def main():
    print("Starting program")

    setup_gpio()
    print("GPIO configured")

    print("Connecting GoPro...")
    connect_gopro()
    blink_led()
    print("-> Connected")

    print("Initializing GoPro settings...")
    init_gopro_settings()
    print("-> Initialized")

    try:
        while True:
            is_encoding = gopro.is_encoding
            print(f"is encoding = {is_encoding}")
            if GPIO.input(SHUTTER_PIN):
                if is_encoding:
                    print("Recording in progress")
                    if GPIO.input(HILIGHT_PIN):
                        if READY_FOR_HILIGHT:
                            print("send hilight event")
                            tag_hilight()
                            READY_FOR_HILIGHT = False
                    else:
                        READY_FOR_HILIGHT = True
                else:
                    print("send start recording")
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    start_recording()
            else:
                if is_encoding:
                    print("send stop recording")
                    GPIO.output(LED_PIN, GPIO.LOW)
                    stop_recording()
                    READY_FOR_HILIGHT = True

            print(".")
            sleep(0.5)
    except:
        print("exception raise exiting program")
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.cleanup()
        gopro.close()
        #sleep then try to restart the script
        sleep(2)
        os.execl(sys.executable, 'python', __file__, *sys.argv[1:])

if __name__ == "__main__":
    sys.exit(main())
j
