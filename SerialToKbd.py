# Copyright (c) 2011 Hesky Fisher.
# Copyright (c) 2017 Carl Hauser.
# See LICENSE.txt for details.
#
# This file is derived from winkeyboardcontrol.py - capturing and
# injecting keyboard events in windows - from version 3 of Plover, the open source
# steno project.
# I (Carl Hauser) have changed it to serve as a standalone forwarder of characters
# from a serial port to the keyboard input of the currently in-focus window

"""Keyboard capture and control in windows.

This module provides an interface for basic keyboard event capture and
emulation. Set the key_up and key_down functions of the
KeyboardCapture class to capture keyboard input. Call the send_string
and send_backspaces functions of the KeyboardEmulation class to
emulate keyboard input.

"""

import ctypes
import multiprocessing
import os
import threading

from ctypes import windll, wintypes

# Python 2/3 compatibility.
from keyboardlayout import KeyboardLayout

SendInput = windll.user32.SendInput
LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT))

class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))

class KeyboardEmulation(object):

    def __init__(self):
        self.keyboard_layout = KeyboardLayout()

    # Sends input types to buffer
    @staticmethod
    def _send_input(*inputs):
        len_inputs = len(inputs)
        len_pinput = INPUT * len_inputs
        pinputs = len_pinput(*inputs)
        c_size = ctypes.c_int(ctypes.sizeof(INPUT))
        return SendInput(len_inputs, pinputs, c_size)

    # Input type must be keyboard
    @staticmethod
    def _input(structure):
        if isinstance(structure, KEYBDINPUT):
            return INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure))
        raise TypeError('Cannot create INPUT structure!')

    # Keyboard input type to send key input
    @staticmethod
    def _keyboard_input(code, flags):
        if flags == KEYEVENTF_UNICODE:
            # special handling of Unicode characters
            return KEYBDINPUT(0, code, flags, 0, None)
        return KEYBDINPUT(code, 0, flags, 0, None)

    # Abstraction to set flags to 0 and create an input type
    def _keyboard(self, code, flags=0):
        return self._input(self._keyboard_input(code, flags))

    def _key_event(self, keycode, pressed):
        flags = 0 if pressed else KEYEVENTF_KEYUP
        self._send_input(self._keyboard(keycode, flags))

    # Press and release a key
    def _key_press(self, char):
        vk, ss = self.keyboard_layout.char_to_vk_ss[char]
        keycode_list = []
        keycode_list.extend(self.keyboard_layout.ss_to_vks[ss])
        keycode_list.append(vk)
        # Press and release all keys.
        for keycode in keycode_list:
            self._key_event(keycode, True)
            self._key_event(keycode, False)

    def _refresh_keyboard_layout(self):
        layout_id = KeyboardLayout.current_layout_id()
        if layout_id != self.keyboard_layout.layout_id:
            self.keyboard_layout = KeyboardLayout(layout_id)

    def _key_unicode(self, char):
        inputs = [self._keyboard(ord(code), KEYEVENTF_UNICODE)
                  for code in char]
        self._send_input(*inputs)

    def send_string(self, s):
        self._refresh_keyboard_layout()
        for char in s:
            if char in self.keyboard_layout.char_to_vk_ss:
                # We know how to simulate the character.
                self._key_press(char)
            else:
                # Otherwise, we send it as a Unicode string.
                self._key_unicode(char)

    def send_key_combination(self, combo_string):
        """Emulate a sequence of key combinations.
        Argument:
        combo_string -- A string representing a sequence of key
        combinations. Keys are represented by their names in the
        self.keyboard_layout.keyname_to_keycode above. For example, the
        left Alt key is represented by 'Alt_L'. Keys are either
        separated by a space or a left or right parenthesis.
        Parentheses must be properly formed in pairs and may be
        nested. A key immediately followed by a parenthetical
        indicates that the key is pressed down while all keys enclosed
        in the parenthetical are pressed and released in turn. For
        example, Alt_L(Tab) means to hold the left Alt key down, press
        and release the Tab key, and then release the left Alt key.
        """
        # Make sure keyboard layout is up-to-date.
        self._refresh_keyboard_layout()
        # Parse and validate combo.
        key_events = parse_key_combo(combo_string, self.keyboard_layout.keyname_to_vk.get)
        # Send events...
        for keycode, pressed in key_events:
            self._key_event(keycode, pressed)


def get_option_info(port):
    """Get the default options for this machine."""
    return {
            'port': (port), 
            'baudrate': (9600),
            'bytesize': (8),
            'parity': ('N'),
            'stopbits': (1),
            'timeout': (2.0),
            'xonxoff': (False),
            'rtscts': (False)
           }

import serial
def capture(port):
        global keepAlive
        serial_params = get_option_info(port)
        try:
            serial_port = serial.Serial(**serial_params)
        except serial.SerialException as SE:
            print ('Can\'t open serial port: %s' % port)
            print ("Serial exception occurred.")
            print (SE.strerror)
            return
        except OSError as OSE:
            print ("OSError occurred")
            print (OSE.strerror)
            return

        if not serial_port.isOpen():
            print('Serial port is not open: %s' & self.serial_params.get('port'))
            return

        kbd_emulator = KeyboardEmulation()
        try:
            while True:

                # Grab data from the serial port.
                raw = serial_port.read(1)
                keepAlive = True
                if not raw:
                    continue

                # Send the character view the keyboard emulator
                kbd_emulator.send_string(chr(raw[0]))
        except KeyboardInterrupt:
            pass

import time
def keepAliveThread():
    global keepAlive
    keepAlive = True
    while keepAlive:
        keepAlive = False
        time.sleep(5)
                
    print("\n%s stopped responding. Was the device unplugged?" % device)
    print("Close and restart this program when the device is again available")
    # sys.stdin.readline()


import serial.tools.list_ports as LP
import sys

import threading
if __name__ == "__main__":
    device = None
    if len(sys.argv) > 1:
        device = sys.argv[1]
    else:
        print ("Looking for a Magtek reader")
        ports = LP.comports()
        for p in ports:
            if p.manufacturer=='MagTek':
               print("Found a MagTek reader with Vendor ID: 0x%x and Product ID: 0x%x on %s" %
                     (p.vid, p.pid, p.device))
               device=p.device
    try:
        if device:
            print("Opening reader on %s" % device)
            print("Type Ctrl-C or close this window to exit")
            # This whole multi-threaded design is ridiculous, but required,
            # because when the device is unplugged, and even perhaps
            # when the system sleeps or hibernates, the serial.read() function
            # hangs, never timing out again.
            threading.Thread(target=keepAliveThread,daemon=True).start()
            capture(device)
        else:
            print("Did not find a supported reader; Use the device manager to identify the COM port")
            print("and then enter the command")
            print("    SerialToKbd COMn")
            print("where n is the number of the COM port you identified in the device manager")
            sys.stdin.readline()
    except KeyboardInterrupt:
        pass

