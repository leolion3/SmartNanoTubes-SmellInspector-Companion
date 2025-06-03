Technical Specification:

- Driver Installation - https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- USB COM port - COMxx (xx is the port number)
- Baud rate - 115200
- Expected output - start;{64 resistance values}; temperature; humidity

The data values are in ASCII format. It begins with "start;" and then all the 64 resistance values are
followed by temperature and humidity values (values positions 65 and 66). All these values are
separated by a semi-colon (;). 

- The total duration for one read-out is approximately 1.8 seconds.

While recording an event (when you press F1 for a short duration of time), "event" will be written on
the serial monitor.

While giving commands to operate the fan, i.e., "FAN1", "FAN2", "FAN3", "FAN0", the fan will initially
operate at full speed for 1 second before going to its specified speed. If the fan is operating at speed
1 and we give the command "FAN2", the fan will go to its full speed for 1 second first and then operate
at a speed corresponding to the "FAN2" command. This functionality is also implemented in Bluetooth
operating mode.
All the commands provided to the Smell Inspector via USB have a newline ("\n") character at the end
of the command.

Commands: 

- "FAN1" 
- "FAN2"
- "FAN3"
- "FAN0"
- "GET_INFO"