import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A


# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D8)
pn532 = PN532_SPI(spi, cs_pin, debug=True)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card to write to!")

key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

while True:
  # Check if a card is available to read
  uid = pn532.read_passive_target(timeout=0.5)
  print(".", end="")
  # Try again if no card is available.
  if uid is not None:
    break

print("")

print("Found card with UID:", [hex(i) for i in uid])
print("Authenticating block 4 ...")

authenticated = pn532.mifare_classic_authenticate_block(uid, 7, MIFARE_CMD_AUTH_A, key)
if not authenticated:
  print("Authentication failed!")

# Set 16 bytes of block to 0xFEEDBEEF
data = bytearray(16)
data[0:16] = b"\xFE\xED\xBE\xEF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

# Write 16 byte block.
pn532.mifare_classic_write_block(7, data)
# Read block #6
print(
  "Wrote to block 4, now trying to read that data:",
  [hex(x) for x in pn532.mifare_classic_read_block(7)],
)