"""
Module: Config file
Description: Contains environment settings
            for different systems
"""

USB_PORT = '/dev/cu.usbmodem0F00F7C51' #MAC PORT
#USB_PORT = '/dev/cu.usbmodem0F0100DE1' #MAC PORT

FIELDNAMES = ['time',
            'ForwardPower',
            'ReversePower',
            'vswr',
            'attenuation',
            'SysTemp',
            'VSWRTemp',
            'VSWRStatus']