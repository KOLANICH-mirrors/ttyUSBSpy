ttyUSBSpy : Python ttyUSB0 serial port Spy
------------------

ttyUSBSpy is a serial port spy, it works on usb-serial converters. It relays in 
the power of the usbmon module. tcpdump captures data betwen the usb and conversor
chip and ttyUSBSpy filters the captured data and show the data and signals of 
Rs232 port.


RUNNING:

   extract the archive and run "python DlgttyUsbSpy.py"  
   to activate capture mode "sudo python DlgttyUsbSpy.py"



USAGE:

   as a practical approach, you would probably: 
 
   1) capture data with capture mode or using the wireshark and capturing the
   usb data
      
 
   2) Charge captured file, ttyUSBSpy decodes the file and shows data and signals.


v0.01e:
  - Last line bug, repaired.
  - Shows CTS Signal.
  


