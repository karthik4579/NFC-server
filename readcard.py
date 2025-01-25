import board
import busio
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from firebasecmp import validate_password
import RPi.GPIO as GPIO
from time import sleep
from firebaselog import log


spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D8)
pn532 = PN532_SPI(spi, cs_pin, debug=False)


# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

Red_led_pin = 24
Blue_led_pin = 25
Yellow_led_pin = 23
Solenoid_pin = 16
Buzzer_pin = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Red_led_pin, GPIO.OUT)
GPIO.setup(Blue_led_pin, GPIO.OUT)
GPIO.setup(Yellow_led_pin, GPIO.OUT)
GPIO.setup(Solenoid_pin, GPIO.OUT)
GPIO.setup(Buzzer_pin, GPIO.OUT)

def read_card():
    global uid
    extracted_password = []
    GPIO.output(Blue_led_pin,True)
    sleep(0.5)
    while True:
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            if uid is not None:
                break
            
        #for block_no in range(4,13):
            pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_A, key)
            nfc_card_data = str(pn532.mifare_classic_read_block(4),'utf-8').replace("#", "")
            extracted_password.append(nfc_card_data)

            pn532.mifare_classic_authenticate_block(uid, 5, MIFARE_CMD_AUTH_A, key)
            nfc_card_data = str(pn532.mifare_classic_read_block(5),'utf-8').replace("#", "")
            extracted_password.append(nfc_card_data)
        
        final_extracted_password = ''.join(extracted_password)
        print(final_extracted_password)
        '''
        username = list(final_extracted_password.split(":"))[0]

        password_validation_status = validate_password(final_extracted_password)

        if password_validation_status == None:
            uid = None
            GPIO.output(Buzzer_pin,True)
            sleep(0.3)
            GPIO.output(Buzzer_pin,False)
            sleep(0.3)
            GPIO.output(Buzzer_pin,True)
            sleep(0.3)
            GPIO.output(Buzzer_pin,False)
            continue

        else:
            uid = None
            GPIO.output(Solenoid_pin,True)
            GPIO.output(Buzzer_pin,True)
            sleep(1)
            GPIO.output(Buzzer_pin,False)
            log(username)
            GPIO.output(Yellow_led_pin,True)
            sleep(5)
            GPIO.output(Yellow_led_pin,False)
            sleep(1)
            GPIO.output(Solenoid_pin,False)
            continue
'''
if __name__ == '__main__':
    read_card()
