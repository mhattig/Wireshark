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

########################################################################
# Mainline
########################################################################
def main () :
    ######### UPDATE these values when starting 
    input_dir = '2019-03-24_21_12_09_merged_macs'
    output_dir = '2019-03-24_21_12_09_transformed'
    display_filter = '-Y \"wlan.fc.type_subtype != 0x001d\" -Y \"wlan.fc.type_subtype != 0x0005\" -Y \"frame.len != 53\" -Y \"wlan.fc.type_subtype != 0x001b\" -Y \"wlan.fc.type_subtype != 0x001c\"'

    if os.path.exists(input_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        input_file_list = "%s/input_file_list.txt" % input_dir
        s_cmnd = "ls %s/*.pcapng > %s" % (input_dir, input_file_list)
        print s_cmnd
        os.system(s_cmnd)

        input_file_names = []
        with open(input_file_list) as fd :
            for line in fd:
                input_file_name, junk = line.split('\n')
                input_file_names.append(input_file_name)

        for input_file_name in input_file_names :
            #print "input_file_name = %s" % input_file_name 
            junk, output_file_name_no_dir = input_file_name.split('/')
            #print "output_file_name_no_dir = %s" % output_file_name_no_dir 
            output_file_name_no_ext, junk = output_file_name_no_dir.split('.')
            #print "output_file_name_no_ext = %s" % output_file_name_no_ext 
            output_file_name = "%s/%s.txt" % (output_dir, output_file_name_no_ext)
            s_cmnd = "tshark %s -r %s > %s" % (display_filter, input_file_name, output_file_name)
            print "tshark = %s" % s_cmnd
            os.system(s_cmnd)
    else:
        print "Missing input directory"

if __name__ == "__main__":
    main ()
