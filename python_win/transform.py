# File: transform.py
#
# The MIT License
# 
# Copyright (c) 2010-2018 Google, Inc. http://angularjs.org
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Requires Phython 2.7
#
# This file utilizes the output from get_packet_capture_files.py, which puts a series of 
# wireshark capture (.pcapng) files into a common directory. input_dir is the variable 
# name for the directory with the output from get_packet_capture_files.py.
#
# Extraction takes place in two steps with output from the first step going to a temp directory 
# and then an output from the second step in the output directory. The variable names temp_dir 
# and output_dir are set to these directory names. 
#
# A good practice for the names of the temp_dir and output_dir is to use something common in 
# input directory name like the time component. This allows for an easy association
# between sets of input, temp, and output data. When doing multiple long packet captures this 
# association help to stay organized.
#
# Temp directory has wireshark files (.pcapng) with only packets from a particular mac address.
# So if there are 54 files (20 minutes for 18 hours) and two MAC addresses (e.g. STA one, STA two)
# then the temp directory has 108 files. All the packets from the AP are included in each file
# because some AP packets used by a STA do not have the STA mac address.
#
# Output directory has one wireshark file (.pcapng) for each STA mac address. Output file is a 
# splice-together of all packets for a single STA MAC and AP MAC for the duration of the entire test.
#
# Steps
#   1. Set the values for the input_dir and output_dir. Name of input_dir must match the
#      desired output from mac_traces.py.
#   2. Modify display filter to select desired packets in the text output
#
import os
import re
import sys

_THIS_FILE_LOCATION_ = os.path.dirname(os.path.realpath(__file__))
_DATA_LOCATION_ = os.path.join(os.path.dirname(_THIS_FILE_LOCATION_), 'data')
_WIRESHARK_INSTALL_LOCATION_ = "C:\Program Files\Wireshark"

########################################################################
# Mainline
########################################################################
def main () :
    ######### UPDATE these values when starting 
    input_dir = os.path.join(_DATA_LOCATION_, '2019-03-25_19_59_42_macs')
    output_dir = os.path.join(_DATA_LOCATION_, '2019-03-25_19_59_42_transformed')

    # display_filter:
    # Probe Request: type_subtype = 0x4
    # Probe Response: type_subtype = 0x5
    # Ack: type_subtype= 0x1d
    # Block Ack: type_subtype= 0x19
    # RTS: type_subtype= 0x1b
    # CTS: type_subtype= 0x1c
    # Null Frames: (frame.len == 53)
    # 
    display_filter = ' -Y \"!(wlan.fc.type_subtype == 0x0019) && !(wlan.fc.type_subtype == 0x001c) && !(wlan.fc.type_subtype == 0x001b) && !(wlan.fc.type_subtype == 0x001d) && !(wlan.fc.type_subtype == 0x0005) && !(wlan.fc.type_subtype == 0x0005) && !(frame.len == 53) \" '
    display_dhcp_dns = ' -Y \" (udp.port == 53 || udp.port == 68 || udp.port == 67) \" '

    if os.path.exists(input_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        input_file_names = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('pcapng')]

        for input_file_name in input_file_names :
            output_file_name_no_dir = os.path.basename(input_file_name)
            output_file_name_no_ext = os.path.splitext(output_file_name_no_dir)[0]
            output_file_name_with_ext = output_file_name_no_ext + '.txt'
            output_file_name = os.path.join(output_dir, output_file_name_with_ext)

            # This is needed to make tshark command run on windows
            if(sys.platform == 'win32'):
                os.chdir(_WIRESHARK_INSTALL_LOCATION_)

            s_cmnd = "tshark -r %s %s > %s" % (input_file_name, display_filter, output_file_name)
            print("tshark = %s" % s_cmnd)
            os.system(s_cmnd)
    else:
        print("Missing input directory")

if __name__ == "__main__":
    main ()
