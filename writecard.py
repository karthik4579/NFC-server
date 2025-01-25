import board
import busio
import textwrap
import time
import sys
from digitalio import DigitalInOut
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A
from adafruit_pn532.spi import PN532_SPI
import RPi.GPIO as GPIO


spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D8)
pn532 = PN532_SPI(spi, cs_pin, debug=True)
pn532.SAM_configuration()  # Configure PN532 to communicate with MiFare cards

Red_led_pin = 24
Blue_led_pin = 25

GPIO.setup(Red_led_pin, GPIO.OUT)
GPIO.setup(Blue_led_pin, GPIO.OUT)

key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

def add_padding(password_segment):
        input_password_segment = password_segment
        password_length= len(password_segment)
        if password_length < 16:
            index = 16-password_length
            for i in range(index):
                input_password_segment = input_password_segment + '#'
            return bytearray(input_password_segment.encode())
        else:
            return bytearray(input_password_segment.encode())

    
def write_card(password, activity):
    GPIO.output(Blue_led_pin,False)
    time.sleep(0.5)
    GPIO.output(Red_led_pin,True)
    time.sleep(0.5)
    while True:
        # Check if password card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is not None:
            break
        else:
            continue

    if activity == "reset":
        final_data_segments = {}
        raw_password_segments = textwrap.wrap(str(password), width=16)
              
        for raw_segment in zip(raw_password_segments,(blockno for blockno in range(4,13))):
            padded_password_segments = add_padding(raw_segment[0])
            final_data_segments[str(raw_segment[1])] = padded_password_segments


        for block_no,data in final_data_segments.items():
            authenticated = pn532.mifare_classic_authenticate_block(uid, int(block_no), MIFARE_CMD_AUTH_A, key) # authenticate block with default key
            if not authenticated:
                print('not authenticated')
                break
            print('the data being written is :',data)
            print('the block no is :',int(block_no))
            pn532.mifare_classic_write_block(int(block_no), data) # Write 16 bytes of data to the designated block

        GPIO.output(Red_led_pin,False)
        GPIO.output(Blue_led_pin,True)
        time.sleep(1)
        return "done"

    elif activity == "register":
        final_data_segments = []
        raw_password_segments = textwrap.wrap(str(password), width=16)

        for raw_segment in raw_password_segments:
            padded_password_segments = add_padding(raw_segment)
            final_data_segments.append(padded_password_segments)
        
        
            pn532.mifare_classic_authenticate_block(uid, block_no, MIFARE_CMD_AUTH_B, key) # authenticate block with default key
            pn532.mifare_classic_write_block(block_no, final_data_segments[0]) # Write 26 bytes of data to the designated block
            
            pn532.mifare_classic_authenticate_block(uid, block_no, MIFARE_CMD_AUTH_B, key) # authenticate block with default key
            pn532.mifare_classic_write_block(block_no, final_data_segments[1]) # Write 26 bytes of data to the designated block

            pn532.mifare_classic_authenticate_block(uid, block_no, MIFARE_CMD_AUTH_B, key) # authenticate block with default key
            pn532.mifare_classic_write_block(block_no, final_data_segments[2]) # Write 26 bytes of data to the designated block

        GPIO.output(Red_led_pin,False)
        GPIO.output(Blue_led_pin,True)
        time.sleep(1)
        return uid

if __name__ == '__main__':
    cmdline_inputs = sys.argv
    if cmdline_inputs[2] == "reset":
        status = write_card(cmdline_inputs[1],cmdline_inputs[2])
        print(status)
    elif cmdline_inputs[2] == "register":
        status = write_card(cmdline_inputs[1],cmdline_inputs[2])
        print(status)