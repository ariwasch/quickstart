#!/usr/bin/env python3
"""
Test script for ODrive GPIO-based communication.

This script demonstrates how to control an ODrive using only GPIO pins 1 and 2
rather than the full UART communication.
"""

import time
import sys
import os

# Add the parent directory to the path so we can import the library modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.control.odrive_uart import ODriveGPIO
from RPi import GPIO

def main():
    """
    Main function to test the ODriveGPIO class.
    """
    print("Starting ODrive GPIO test...")
    print("This test will control the ODrive using GPIO1 and GPIO2 pins.")
    
    try:
        # Initialize the ODriveGPIO class
        # Here we're connecting ODrive's GPIO1 to Raspberry Pi's GPIO0
        # and ODrive's GPIO2 to Raspberry Pi's GPIO1
        odrive = ODriveGPIO(odrive_gpio1_pin=0, odrive_gpio2_pin=1)
        
        # Stop any current movement
        print("Stopping motors...")
        odrive.stop()
        time.sleep(1)
        
        # Move left motor forward
        print("Moving left motor forward...")
        odrive.move_left(direction=1, speed=0.3)
        time.sleep(2)
        
        # Stop
        print("Stopping...")
        odrive.stop()
        time.sleep(1)
        
        # Move left motor backward
        print("Moving left motor backward...")
        odrive.move_left(direction=-1, speed=0.3)
        time.sleep(2)
        
        # Stop
        print("Stopping...")
        odrive.stop()
        time.sleep(1)
        
        # Move right motor forward
        print("Moving right motor forward...")
        odrive.move_right(direction=1, speed=0.3)
        time.sleep(2)
        
        # Stop
        print("Stopping...")
        odrive.stop()
        time.sleep(1)
        
        # Move right motor backward
        print("Moving right motor backward...")
        odrive.move_right(direction=-1, speed=0.3)
        time.sleep(2)
        
        # Stop
        print("Stopping...")
        odrive.stop()
        time.sleep(1)
        
        # Move both motors
        print("Moving both motors...")
        odrive.move_left(direction=1, speed=0.3)
        odrive.move_right(direction=1, speed=0.3)
        time.sleep(2)
        
        # Emergency stop
        print("Emergency stop!")
        odrive.emergency_stop()
        
        print("GPIO test completed successfully.")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        GPIO.cleanup()
        print("GPIO cleaned up")

if __name__ == "__main__":
    main() 