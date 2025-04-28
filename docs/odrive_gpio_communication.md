# Communicating with ODrive using GPIO1 and GPIO2 pins

This document explains how to communicate with an ODrive motor controller using only GPIO1 and GPIO2 pins, without using the standard UART communication.

## Overview

ODrive controllers typically communicate with host systems (like Raspberry Pi) using UART serial communication. However, in some cases, you might want to use just the GPIO pins for simpler signaling. This approach has limitations but can work for basic control scenarios.

## Hardware Connection

1. Connect ODrive's GPIO1 to Raspberry Pi's GPIO0 (BCM numbering)
2. Connect ODrive's GPIO2 to Raspberry Pi's GPIO1 (BCM numbering)
3. Ensure you have a common ground connection between the ODrive and Raspberry Pi

Make sure your ODrive firmware version supports GPIO pin functionality. The standard firmware may need customization to interpret the GPIO signals as motor commands.

## How the GPIO Communication Works

Since we're limited to just two GPIO pins, we use a simple pulse-based protocol to send commands. Each command is represented by a specific pattern of HIGH and LOW states on the GPIO pins, with specific timing.

The basic concept is:

1. Use unique patterns of pulses to represent different commands
2. The duration, sequence, and combination of pulses on GPIO1 and GPIO2 encode different commands
3. Use a simple state machine on both sides to interpret the commands

## Customizing the Protocol

The example implementation in `ODriveGPIO` class provides a basic framework, but you'll likely need to adapt the signal patterns to work with your specific ODrive configuration.

### Example Commands

| Command | GPIO1 Pattern | GPIO2 Pattern |
|---------|--------------|--------------|
| Move Left Forward | HIGH→LOW→HIGH | HIGH |
| Move Left Backward | HIGH→LOW→LOW | HIGH |
| Move Right Forward | HIGH | HIGH→LOW→HIGH |
| Move Right Backward | HIGH | HIGH→LOW→LOW |
| Stop | LOW | LOW |
| Emergency Stop | LOW | LOW (extended duration) |

## ODrive Firmware Considerations

For this approach to work, you'll need to modify the ODrive firmware to:

1. Monitor GPIO1 and GPIO2 pins
2. Interpret the pulse patterns according to your protocol
3. Execute the corresponding motor commands

The ODrive firmware is open-source and can be modified to support GPIO-based command interpretation. You'll need to add a state machine to the firmware that monitors these pins and takes appropriate motor control actions based on the patterns received.

## Limitations

Using just GPIO pins has significant limitations compared to full UART communication:

1. Limited command set - you can only encode a few distinct commands
2. No feedback - difficult to get status information back from the ODrive
3. Lower reliability - no error checking or retry mechanisms
4. Timing-sensitive - pattern recognition depends on precise timing

## Alternative: Combined Approach

A more reliable approach might be to:

1. Use UART for configuration, calibration, and error handling
2. Use GPIO pins for real-time control signals or emergency stops

This gives you the best of both worlds - reliable configuration via UART and fast responsiveness via GPIO.

## Testing Your Setup

Use the provided `test_odrive_gpio.py` script to test your GPIO communication:

```bash
python3 scripts/test_odrive_gpio.py
```

This will cycle through various motor movements using the GPIO communication.

## Troubleshooting

If your motors don't respond to GPIO commands:

1. Check physical connections between Raspberry Pi and ODrive
2. Verify GPIO pin numbers match your actual connections
3. Ensure the ODrive firmware supports GPIO command interpretation
4. Use an oscilloscope or logic analyzer to verify the pulse patterns
5. Try different timing parameters for the pulse patterns
6. Check if the ODrive is in a valid operational state (e.g., not in error mode)

## Further Development

To extend this concept, consider:

1. Implementing a more sophisticated protocol using pulse-width modulation (PWM)
2. Adding checksums or validation patterns to increase reliability
3. Using multiple GPIO pins (if available) to increase the command space

## Resources

- [ODrive Documentation](https://docs.odriverobotics.com/)
- [ODrive GitHub Repository](https://github.com/odriverobotics/ODrive)
- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/hardware/raspberrypi/gpio/README.md) 