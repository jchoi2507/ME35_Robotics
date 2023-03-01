'''

ME35HW6.py

Waits for Airtable API field input.

1) Opens serial communication with RP2040
2) Executes main() function on RP2040

'''

import requests
import time
import serial
from mySecrets import *

        ## FOR ME35 CLASS CONFIGURATIONS ##

# URL = 'https://api.airtable.com/v0/' + AT_Keys['BaseID'] + '/DataTable'
# headers = {"Authorization":"Bearer " + AT_Keys['Token']}

        ## MY OWN DEMO CONFIGURATIONS ##

URL = myURL
headers = myHeaders

        ## MAIN ##

s = serial.Serial('/dev/cu.usbmodem14401', 115200)

# APIListen() waits until the Airtable field is == 1
def APIListen():
	keepLooping = True
	while (keepLooping):
		r = requests.get(URL, headers=headers)
		data = r.json()
		field = data['records'][1]['fields']['value']

		if (field == 1): # Airtable field of int: 1 -> start serial communication w/ RP2040
			keepLooping = False

		else:
			print("Waiting for command to execute...")

		time.sleep(0.5)

# startRP2040() executes the main() function in "CrazyCar.py" on the RP2040
def startRP2040():
	print("Executing command...")
	print(s.read_all())
	s.write(b'import RP2040_CrazyCar\r\n')
	s.write(b'RP2040_CrazyCar.main()\r\n') # Run main() in RP2040_CrazyCar.py

if __name__ == "__main__":
	APIListen()
	startRP2040()
