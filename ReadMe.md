ttyUSBSpy : Python ttyUSB0 serial port Spy
-------------------------------------------

This is a [python 3 ready](https://python3statement.org/) version of https://sourceforge.net/projects/ttyusbspy (Original authors are unknown at least to me (I couldn't find their online accounts)).

`ttyUSBSpy` is a tool showing [usbmon](https://www.kernel.org/doc/Documentation/usb/usbmon.txt) [pcap](https://wiki.wireshark.org/Development/LibpcapFileFormat) captures of communications with [Prolific](http://www.prolific.com.tw/) [PL2303*](http://www.prolific.com.tw/US/ShowProduct.aspx?pcid=41&showlevel=0017-0037-0041) USB-serial converters.


RUNNING:
   * capture USB communications with [usbmon](https://www.kernel.org/doc/Documentation/usb/usbmon.txt).
   * just run `python3 -m ttyUSBSpy` and you will be able to load your capture there.
   * to activate capture mode run `sudo python3 -m ttyUSBSpy`



USAGE:

    as a practical approach, you would probably:

    1. capture data with capture mode or using the [Wireshark]() and capturing the USB data

    2. Charge captured file, ttyUSBSpy decodes the file and shows data and signals.


