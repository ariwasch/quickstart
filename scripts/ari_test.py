import serial
import glob
import time

# Only look at typical UART devices
ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyAMA*') + glob.glob('/dev/ttyTHS*')

for port in ports:
    try:
        print(f"Trying {port}...")
        ser = serial.Serial(port, baudrate=115200, timeout=0.5)  # shorter timeout
        time.sleep(0.1)

        ser.write(b'r vbus_voltage\n')
        time.sleep(0.1)

        response = ser.readline()
        if response:
            print(f"Got response from {port}: {response.decode().strip()}")
        else:
            print(f"No response from {port}")
        ser.close()
    except Exception as e:
        print(f"Error on {port}: {e}")
