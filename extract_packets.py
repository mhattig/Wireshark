# File: extract_packets.py
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
#   1. Add STAs mac addresses to capture to the variable macs = []
#   2. Set the AP mac address to the variable AP_mac
#   3. Set the values for the input_dir, temp_dir, and output_dir. Name of input_dir must match the
#      desired output from get_packet_capture_files.py.
#
import os
import re

########################################################################
# Mainline
#   1. Start wireshark before turning on the in order to capture the 4-way handshake
##########################################################################################
def main () :
    ######### UPDATE these values when starting a new query
    input_dir = "2018-10-08_14_48_02_packets"
    temp_dir = "temp_14_48_02"
    output_dir = "output_14_48_02"
    # MAC of STAs and APs that are to be captured
    # replace these with correct MACs
    macs = ["01:02:03:04:05:06", "07:08:09:10:11:12"]
    AP_mac = "13:14:15:16:17:18" 

    if os.path.exists(input_dir):
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        input_file_list = "%s/input_file_list.txt" % temp_dir
        s_cmnd = "ls %s/*.pcapng > %s" % (input_dir, input_file_list)
        print s_cmnd
        os.system(s_cmnd)

        input_file_names = []
        with open(input_file_list) as fd :
            # get the original capture files that have all packets for a given period of time
            for line in fd:
                input_file_name, crap = line.split('\n')
                input_file_names.append(input_file_name)

        i = 1
        for mac in macs :
            temp_file_names = []
            mac_str = re.sub(':','_',mac)
            j = 1
            for input_file_name in input_file_names :
                # create temp file that extracts the packets with AP mac address and/or
                # one STA mac address. i and j make filename unique so data is not 
                # overwritten.
                temp_file_name = "%s/temp_%s_%d_%d.pcapng" % (temp_dir, mac_str, i, j)
                temp_file_names.append(temp_file_name)
                s_cmnd = "tshark -Y \"wlan.addr == %s\" -Y \"wlan.addr == %s\" -r %s -w %s" % 
                    (AP_mac, mac, input_file_name, temp_file_name)
                print "tshark = %s" % s_cmnd
                os.system(s_cmnd)
                j += 1
            # merge all the temp files from one mac address together
            merge_cmnd_str = "mergecap -w %s/%s_packets.pcapng" % (output_dir, mac_str)
            for temp_file_name in temp_file_names :
                merge_cmnd_str += " %s" % temp_file_name
            print "Merge = %s" % merge_cmnd_str
            os.system(merge_cmnd_str)
            i += 1
    else:
        print "Missing input directory"

if __name__ == "__main__":
    main ()
