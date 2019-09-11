#! /usr/bin/python
 
"""
    This utility will query a XBee radio for some of it's AT Command parameters and print their values, as well as
    optional discriptive information.  It has a set of default AT Commands or the use can provide the desired set
    of AT Commands on the command-line.
 
    The dictionay of AT Command descriptive information is limited but can be easily expanded.  The descriptive
    information was taken from the first referance given below. Also note that if this utility appears to hang,
    it is almost certainly waiting on a response from the XBee. To continue processing the AT Command list, use Ctrl-C.
 
    Reference Materials:
        XBee/XBee-PRO OEM RF Modules: Product Manual v1.xCx - 802.15.4 Protocol
            ftp://ftp1.digi.com/support/documentation/90000982_A.pdf
        python-xbee Documentation: Release 2.0.0, Paul Malmsten, December 29, 2010
 
http://python-xbee.googlecode.com/files/XBee-2.0.0-Documentation.pdf
 
        Parser for command-line options, arguments and sub-commands
 
http://docs.python.org/2/library/argparse.html#module-argparse
 
"""
 
# imported modules
import os                       # portable way of using operating system dependent functionality
import sys                      # provides access to some variables used or maintained by the Python interpreter
import serial                   # encapsulates the access for the serial port
import argparse                 # provides easy to write and user-friendly command-line interfaces
from xbee import XBee           # implementation of the XBee serial communication API
from pretty import stringc      # provides colored text for xterm and VT100 type terminals using ANSI Escape Sequences
 
# authorship information
__author__ = "Jeff Irland"
__copyright__ = "Copyright 2013"
__credits__ = "Paul Malmsten"
__license__ = "GNU General Public License"
__version__ = "0.1"
__maintainer__ = "Jeff Irland"
__email__ = "jeff.irland@gmail.com"
__status__ = "Development"
__python__ = "Version 2.7.3"
 
# text colors to be used during terminal sessions
NORMAL_TEXT = 'normal'
CMD_TEXT = 'bright red'
NAME_TEXT = 'bright yellow'
CAT_TEXT = 'bright yellow'
DESC_TEXT = 'normal'
RANGE_TEXT = 'bright cyan'
DEFAULT_TEXT = 'bright green'
 
class ArgsParser():
    """Within this object class you should load all the command-line switches, parameters, and arguments to operate this utility"""
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="This utility will query a XBee radio for some of it's AT Command parameters and print their values.  It has a set of default AT Commands or the use can provide the desired set of AT Commands on the command-line.", epilog="This utility is for query only and will not change the AT Command parameter values.")
        self.optSwitches()
        self.reqSwitches()
        self.optParameters()
        self.reqParameters()
        self.optArguments()
        self.reqArguments()
    def optSwitches(self):
        """optonal switches for the command-line"""
        self.parser.add_argument("--version", action="version", version=__version__, help="print version number on stdout and exit")
        self.parser.add_argument("-v", "--verbose", action="count", help="produce verbose output for debugging")
        self.parser.add_argument("-n", "--name", required=False, action="store_true", help="print the name (i.e. short description) of the XBee AT Command")
        self.parser.add_argument("-d", "--description", required=False, action="store_true", help="print the full description of the XBee AT Command")
    def reqSwitches(self):
        """required switches for the command-line"""
        pass
    def optParameters(self):
        """optonal parameters for the command-line"""
        self.parser.add_argument("-b", "--baudrate", required=False, action="store", metavar="RATE", type=int, default=9600, help="baud rate used to communicate with the XBee radio")
        self.parser.add_argument("-p", "--device", required=False, action="store", metavar="DEV", type=str, default='/dev/ttyUSB0', help="open this serial port or device to communicate with the XBee radio")
    def reqParameters(self):
        """required parameters for the command-line"""
        pass
    def optArguments(self):
        """optonal arguments for the command-line"""
        self.parser.add_argument(nargs="*", action="store", dest="inputs", help="AT Commands to be queried")
    def reqArguments(self):
        """required arguments for the command-line"""
        pass
    def args(self):
        """return a object containing the command-line switches, parameters, and arguments"""
        return self.parser.parse_args()
 
class ATDict():
    """Within this object class you should load a dictionary of { "AT Command" : [ "Name", "Category", "Description", "Parameter Range", "Default Value" ] }"""
    # Networking & Security, RF Interfacing, Sleep Modes (NonBeacon), Serial Interfacing, I/O Settings, Diagnostics, AT Command Options
    def __init__(self):
        self.commands = {
        "CH" : [ "Channel", "Networking", "Set/Read the channel number used for transmitting and receiving data between RF modules.", "0x0B - 0x1A", "0x0C" ],
        "ID" : [ "PAN ID", "Networking", "Set/Read the PAN (Personal Area Network) ID. Use 0xFFFF to broadcast messages to all PANs.", "0 - 0xFFFF" , "0x3332" ],
        "DH" : [ "Destination Address High", "Networking", "Set/Read the upper 32 bits of the 64-bit destination address. When combined with DL, it defines the destination address used for transmission. To transmit using a 16-bit address, set DH parameter to zero and DL less than 0xFFFF. 0x000000000000FFFF is the broadcast address for the PAN.", "0 - 0xFFFFFFFF", "0" ],
        "DL" : [ "Destination Address Low", "Networking", "Set/Read the lower 32 bits of the 64-bit destination address. When combined with DH, DL defines the destination address used for transmission. To transmit using a 16-bit address, set DH parameter to zero and DL less than 0xFFFF. 0x000000000000FFFF is the broadcast address for the PAN.", "0 - 0xFFFFFFFF", "0" ],
        "MY" : [ "16-bit Source Address", "Networking", "Set/Read the RF module 16-bit source address. Set MY =0xFFFF to disable reception of packets with 16-bit addresses. 64-bit source address(serial number) and broadcast address (0x000000000000FFFF) is always enabled.", "0 - 0xFFFF", "0" ],
        "SH" : [ "Serial Number High", "Networking", "Read high 32 bits of the RF module's unique IEEE 64-bit address. 64-bit source address is always enabled.", "0 - 0xFFFFFFFF [read-only]", "Factory-set" ],
        "SL" : [ "Serial Number Low", "Networking", "Read low 32 bits of the RF module's unique IEEE 64-bit address. 64-bit source address is always enabled.", "0 - 0xFFFFFFFF [read-only]", "Factory-set" ],
        "RR" : [ "XBee Retries", "Networking", "Set/Read the maximum number of retries the module will execute in addition to the 3 retries provided by the 802.15.4 MAC. For each XBee retry, the 802.15.4 MAC can execute up to 3 retries.", "0 - 6", "0" ],
        "RN" : [ "Random Delay Slots", "Networking", "Set/Read the minimum value of the back-off exponent in the CSMA-CA algorithm that is used for collision avoidance. If RN = 0, collision avoidance is disabled during the first iteration of the algorithm (802.15.4 - macMinBE).", "0 - 3 [exponent]", "0" ],
        "MM" : [ "MAC Mode", "Networking", "Set/Read MAC Mode value. MAC Mode enables/disables the use of a Digi header in the 802.15.4 RF packet. When Modes 0 or 3 are enabled(MM=0,3), duplicate packet detection is enabled as well as certain AT commands.", "0 = Digi Mode, 1 = 802.15.4 (no ACKs), 2 = 802.15.4 (with ACKs), 3 = Digi Mode (no ACKs)", "0" ],
        "NI" : [ "Node Identifier", "Networking", "Stores a string identifier. The register only accepts printable ASCII data. A string can not start with a space. Carriage return ends command. Command will automatically end when maximum bytes for the string have been entered. This string is returned as part of the ND (Node Discover) command. This identifier is also used with the DN (Destination Node) command.", "20-character ASCII string", "-" ],
        "NT" : [ "Node Discover Time", "Networking", "Set/Read the amount of time a node will wait for responses from other nodes when using the ND (Node Discover) command.", "0x01 - 0xFC [x 100 ms]", "0x19" ],
        "CE" : [ "Coordinator Enable", "Networking", "Set/Read the coordinator setting. A value of 0 makes it an End Device but a value of 1 makes it a Coordinator.", "0 = End Device, 1 = Coordinator", "0" ],
        "SC" : [ "Scan Channels", "Networking", "Set/Read list of channels to scan for all Active and Energy Scans as a bitfield. This affects scans initiated in command mode (AS, ED) and during End Device Association and Coordinator startup", "0 - 0xFFFF [bitfield](bits 0, 14, 15 not allowed on the XBee-PRO)", "0x1FFE (all XBee-PRO Channels)" ],
        #"SD" : [ "Scan Duration", "Networking", "Set/Read the scan duration exponent.  For End Device - Duration of Active Scan during Association.  For Coordinator - If ‘ReassignPANID’ option is set on Coordinator [refer to A2 parameter],  SD determines the length of time the Coordinator will scan channels to locate existing PANs. If ‘ReassignChannel’ option is set, SD determines how long the Coordinator will perform an Energy Scan to determine which channel it will operate on.  ‘Scan Time’ is measured as (# of channels to scan] * (2 ^ SD) * 15.36ms). The number of channels to scan is set by the SC command. The XBee can scan up to 16 channels (SC = 0xFFFF).", "0-0x0F [exponent]", "4" ],
        "A1" : [ "End Device Association", "Networking", "Set/Read End Device association options. bit 0 - ReassignPanID (0 - Will only associate with Coordinator operating on PAN ID that matches module ID / 1 - May associate with Coordinator operating on any PAN ID), bit 1 - ReassignChannel(0 - Will only associate with Coordinator operating on matching CH Channel setting / 1 - May associate with Coordinator operating on any Channel), bit 2 - AutoAssociate (0 - Device will not attempt Association / 1 - Device attempts Association until success Note: This bit is used only for Non-Beacon systems. End Devices in Beacon-enabled system must always associate to a Coordinator), bit 3 - PollCoordOnPinWake (0 - Pin Wake will not poll the Coordinator for indirect (pending) data / 1 - Pin Wake will send Poll Request to Coordinator to extract any pending data), bits 4 - 7 are reserved.", "0 - 0x0F [bitfield]", "0" ],
        #"XX" : [ "", "", "", "", "" ],
        #"XX" : [ "", "", "", "", "" ],
        }
    def dictionary(self):
        """return the whole dictionary of command"""
        return self.commands
    def command(self, cmd):
        """return the colorized AT Command"""
        return stringc(cmd, CMD_TEXT)
    def name(self, cmd):
        """return the colorized name of the AT Command"""
        return stringc(self.commands[cmd][0], NAME_TEXT)
    def category(self, cmd):
        """return the colorized category of the AT Command"""
        return stringc(self.commands[cmd][1], CAT_TEXT)
    def description(self, cmd):
        """return the colorized description of the AT Command"""
        return stringc(self.commands[cmd][2], DESC_TEXT)
    def range(self, cmd):
        """return the colorized range of the AT Command"""
        return stringc(self.commands[cmd][3], RANGE_TEXT)
 
    def default(self, cmd):
        """return the colorized devault value of the AT Command"""
        stringc(self.commands[cmd][3], DEFAULT_TEXT)
 
class FrameID():
    """XBee frame IDs must be in the range 0x01 to 0xFF (0x00 is a special case).
    This object allows you to cycles through these numbers."""
    def __init__(self):
        self.frameID = 0
    def inc(self):
        if self.frameID == 255:
            self.frameID = 0
        self.frameID += 1
        return self.frameID
 
def byte2hex(byteStr):
    """Convert a byte string to it's hex string representation"""
    hex = []
    for aChar in byteStr:
        hex.append("%02X " % ord(aChar))
    return ''.join(hex).strip()
 
if __name__ == '__main__':
    # parse the command-line for switches, parameters, and arguments
    parser = ArgsParser()                           # create parser object for the command-line
    args = parser.args()                            # get list of command line arguments, parameters, and switches
    if args.verbose > 0:                         # print what is on the command-line
        print os.path.basename(__file__), "command-line arguments =", args.__dict__
 
    # create required objects
    frameID = FrameID()                             # create a cycling frame ID sequence number to be used in XBee frames
    at = ATDict()                                   # create a dictionary of XBee AT Commands definitions
    ser = serial.Serial(args.device, args.baudrate) # Open the serial port that has the XBee radio
    xbee = XBee(ser)                                # Create XBee object to communicate with the XBee radio
 
    # if user provided desired AT Commands, use them for query, otherwise use the whole dictionary
    if len(args.inputs) == 0:
        args.inputs = at.dictionary()
 
    # for the command list provided, query the XBee radio AT Command's parameters
    for cmd in args.inputs:
        xbee.send('at', frame_id=chr(frameID.inc()), command=cmd)
        try:
            response = xbee.wait_read_frame()
            if args.name:
                print at.command(cmd) + " = " + byte2hex(response['parameter']) + "  " + at.name(cmd)
            else:
                print at.command(cmd) + " = " + byte2hex(response['parameter'])
            if args.description:
                print at.description(cmd) + "\n"
        except KeyboardInterrupt:
            print "*** AT Command \"" + at.command(cmd) + "\" interrupted. ***"
            if args.description:
                print " "
 
    ser.close()