#!/usr/bin/env python3
import serial
import time
import sys

# UART port for pins 8 and 10 on Jetson Orin Nano
UART_PORT = '/dev/ttyTHS1'  # Make sure this is correct for your setup
BAUD_RATE = 115200

def test_uart():
    print(f"Testing UART communication on {UART_PORT} at {BAUD_RATE} baud")
    
    try:
        # Open serial port
        ser = serial.Serial(
            port=UART_PORT,
            baudrate=BAUD_RATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        
        # Make sure port is open
        if not ser.is_open:
            ser.open()
        
        print(f"Serial port {UART_PORT} opened successfully")
        
        # Send test message
        test_message = "UART TEST MESSAGE\n"
        print(f"Sending: {test_message.strip()}")
        ser.write(test_message.encode())
        ser.flush()
        
        # Wait a moment for any response
        time.sleep(0.5)
        
        # Check if any data is waiting to be read
        if ser.in_waiting > 0:
            # Read response
            response = ser.readline().decode().strip()
            print(f"Received: {response}")
        else:
            print("No response received")
        
        # Enter loop for interactive testing
        print("\nEntering interactive mode (Ctrl+C to exit):")
        print("Type a message and press Enter to send it")
        
        while True:
            # Get input from user
            message = input("> ")
            if not message:
                continue
            
            # Add newline to message
            if not message.endswith('\n'):
                message += '\n'
            
            # Send message
            ser.write(message.encode())
            ser.flush()
            
            # Wait for response
            time.sleep(0.1)
            
            # Check for response
            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting).decode().strip()
                print(f"Received: {response}")
            else:
                print("No response")
                
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Close the serial port
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed")

if __name__ == "__main__":
    test_uart() 