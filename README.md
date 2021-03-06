# SerialToKbd

SerialToKbd is a simple helper program that allows MagTek USB check/credit card
readers 22533003 and 22533007 to be used with software that doesn't specifically support check readers.
It is intended as a replacement for the MicrSend program that MagTek used to provide but which no
longer works with recent versions of Windows.

You do NOT need this program if:
* Your app supports the check reader directly (for example PowerChurch versions 10, 11, and 11.5 running locally)
* You have a USB MiniMicr that does keyboard emulation (part number 22523009 or 22523012 and similar)
* You have a keyboard "wedge" MiniMicr (22520001) that plugs into the PS/2 keyboard port of your computer

This program MAY help if you have non-keyboard-emulation USB MiniMicr or a MiniMicr that plugs into
the serial port on your computer AND your app doesn't support the MiniMicr directly (for example
PowerChurch Online and PowerChurch versions 8.5 and 9 running locally) (tested with 22533003 and 22533007
readers and PowerChurch Online).

Before using SerialToKbd you should install the MagTek drivers for your device.

The MiniMicr can format its output in a large number of different ways. The app you intend to use it with
probably requires a specific format. The can be set up using the MicrBase program from MagTek's web site.
Making sure that MicrBase works also helps ensure that all the prerequisites for using SerialToKbd have
been met.

Use: launch SerialToKbd by double-clicking it. It open a console window and tell you what it is doing.

If it does not find your MiniMicr: use the Windows Device Manager to look at the Ports (COM & LPT) on your computer.
The USB Mini Micr should be listed as such. A MiniMicr attached with a serial cable may not be. In this case
try launching SerialToKbd from a command prompt and passing the COM port name (e.g. COM1) as a parameter:
    SerialToKbd COM1

You can test whether the MiniMicr and SerialToKbd are working by
opening NotePad or WordPad and placing the cursor in it. Then scan a check: you should see the check
information appear as characters in the document.

I would be interested in learning the MagTek part numbers of additional readers that this program
can help with as well as their USB Vendor and Product IDs. The Vendor and Product IDs can be found
using the Windows Device Manager. The part number - something like 22xyyzzzz -
can be found on a label on the bottom of the reader.

Please post information as an "Issue" on the project github page:
    http://github.com/chauser/SerialToKbd

This program is derived from pieces of the open source stenography Plover project that turned out to have all the functionality
needed to implement a replacement for MicrSend. Thanks to the Plover creators for their work!

License: see 'License.txt'

Source code for the program may be found at the project github page:
    http://github.com/chauser/SerialToKbd

## Download
Select the 'Releases' tab above and download the zip file for the latest release. Extract the contained files,
then double-click 'SerialToKbd' to run the program. If you need to run from a command prompt in order to
supply a 'COMn' parameter, open a command prompt, change directory to the folder where you extracted the files,
and type
    SerialToKbd COMn
where 'n' is the number of the COM port you want to monitor.

## Running from source and Building

### Run directly from source (assumes you have python installed):
    python SerialToKbd.py
or
    python SerialToKbd.py COMn

### Package as .exe (assumes you have pyinstaller installed)
    pyinstaller -F SerialToKbd.py

The created .exe is 'dist/SerialToKbd.exe'


   
