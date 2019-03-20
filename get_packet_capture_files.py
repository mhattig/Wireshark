# File: get_packet_capture_files.py
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
# Packet captures can only be performed on one WiFi channel at a time. Because
# all data on this channel is capture, capture files get big fast.
#
# Recommend that each individual packet capture file is no more than 20 minutes.
# thus default value for variable sniff_time = 20*60
# 
# The variable test_duration is the time for the entire packet capture. Default is 18 hours. 
#
# The MAC address of the AP must be included because some packet have the AP mac address
# and not the STA MAC address.
# 
# Steps
#   1. Add STA and AP mac addresses to capture to the variable macs = []
#   2. Set the duration of the entire packet capture - default is 18 hours
#   3. Set the time for each individual packet capture - recommend 20 minutes
#
# Resulting capture files are put into a subdirectory with a name that includes the
# time/date that the packet capture was started. Note 18 hours of 20 minute captures
# is 54 files. Capturing packets in an environment with video streaming packets
# creates much larger files than capturing packets that check email.
#
import os
from datetime import datetime, timedelta

########################################################################
# Mainline
########################################################################
def main () :

    ######### UPDATE these values when starting a new test
    # MAC of STAs and APs that are to be captured
    # replace these with correct MACs
    macs = ["01:02:03:04:05:06", "07:08:09:10:11:12"]
    test_duration = 18*60*60  # duration of test time in seconds
    sniff_time = 20*60        # sniff time in seconds

    start_datetime = datetime.now()
    end_datetime = start_datetime + timedelta(seconds=test_duration)
    dir_name_str = '%s_packets/' % start_datetime.strftime('%Y-%m-%d_%H_%M_%S')

    if not os.path.exists(dir_name_str):
            os.mkdir(dir_name_str)

    duration_str = "duration:%d" % sniff_time

    capture_macs_str = ""
    if macs :
        capture_macs_str = 'ether host %s' % macs[0] 
        for mac in macs[1:] :
            capture_macs_str = "%s or ether host %s" % (capture_macs_str, mac)

    curr_datetime = datetime.now()
    while curr_datetime < end_datetime :
        sniffer_file = curr_datetime.strftime('%Y-%m-%d_%H_%M_%S.pcapng')
        print "end time = %s, sniffer file = %s" %  (end_datetime, sniffer_file)
        sniffer_file = "%s%s" % (dir_name_str, sniffer_file)
        if capture_macs_str:
            usrCmd = "dumpcap -i en0 -I -a %s duration:%d -w %s" % (capture_macs_str, 
                    sniff_time, sniffer_file)
        else :
            usrCmd = "dumpcap -i en0 -I -a duration:%d -w %s" % (sniff_time, sniffer_file)
        os.system(usrCmd)
        curr_datetime = datetime.now()


    main ()
