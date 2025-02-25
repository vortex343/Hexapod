import RPi.GPIO as GPIO
import time

SPEAKER_PIN = 19  # Choose a GPIO pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)

pwm = GPIO.PWM(SPEAKER_PIN, 440)  # 440Hz tone
pwm.start(50)  # 50% duty cycle

time.sleep(0.5)

pwm.stop()
GPIO.cleanup()
