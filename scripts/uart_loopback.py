#!/usr/bin/env python3
import serial
import time
import random
import string

"""
UART Loopback Test for Jetson Orin Nano

Instructions:
1. Connect pin 8 (TX) to pin 10 (RX) with a jumper wire
2. Run this script

This creates a loopback where data sent out of TX is received back on RX.
If successful, the test messages will be echoed back.
"""

# UART port for pins 8 and 10 on Jetson Orin Nano
UART_PORT = '/dev/ttyTHS1'  # Adjust if needed for your specific device
BAUD_RATE = 115200

def generate_random_string(length=10):
    """Generate a random string for testing."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_loopback():
    print(f"Starting UART loopback test on {UART_PORT}")
    print("Make sure you've connected pin 8 (TX) to pin 10 (RX) with a jumper wire")
    
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
        
        # Clear any pending data
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Run test 5 times
        for i in range(5):
            # Generate test message with ID to verify exact match
            test_message = f"TEST-{i+1}-{generate_random_string()}\n"
            expected = test_message.strip()
            
            print(f"\nTest {i+1}: Sending: '{expected}'")
            
            # Write the test message
            ser.write(test_message.encode())
            ser.flush()
            
            # Wait for loopback response
            time.sleep(0.1)
            
            # Read response
            if ser.in_waiting > 0:
                response = ser.readline().decode().strip()
                print(f"Received: '{response}'")
                
                # Verify response
                if response == expected:
                    print("✅ PASSED: Received matches sent")
                else:
                    print("❌ FAILED: Received data doesn't match sent data")
            else:
                print("❌ FAILED: No data received")
                
            # Short delay between tests
            time.sleep(0.5)
            
        print("\nLoopback test complete")
        
    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        # Close the serial port
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed")

if __name__ == "__main__":
    test_loopback() 