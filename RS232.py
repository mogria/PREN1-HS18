import serial

# with enable_uart=1 in /boot/config.txt, ttyS0 is the serial
# interface with the raspberry PI
s = serial.Serial('/dev/ttyS0', 9600) # baud rate = 9600, default parity settings
s.read(10) # read 10 byte, blocking
s.write(b"some bytes") # write some bytes b"" is required because unicode is not supported
