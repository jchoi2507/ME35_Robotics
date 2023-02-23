import requests
import time
import serial

# API connection initialization
s = serial.Serial('/dev/cu.usbmodem142301', 9600)
URL = "https://api.agify.io/"

# Function obtains name to send to agify API
def inputName():
    nameToAgify = input("Enter a name!\n")
    return nameToAgify

if __name__ == "__main__":
    while True:
        nameToAgify = inputName()

        param = {"name": nameToAgify}
        response = requests.get(URL, params = param)

        data = response.json()
        predictedAge_str = str(data["age"]) # API response

        count = str(data["count"]) # API response

        s.write(predictedAge_str.encode()) # Sending to Arduino through serial

        print(nameToAgify + " should be " + predictedAge_str + " years old from " + count + " data sets!\n")
        time.sleep(1)
