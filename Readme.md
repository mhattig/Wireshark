This repository provides Wireshark config files and python programs that use Wireshark tools 
and a data sample created by using the python programs. Subdirectories in the repository are:

    config
    python
    data

Here are descriptions of these directories:

config:

This directory contains wireshark configuration files. These files should be copied
into the ~/.config/wireshark directory that gets created after downloading
Wireshark 2.6.6. 

    preferences - defines wireshark window pane layour and columns in the display pane
    colorfilters - associates colors with protocol fields and values for display in 
    Wireshark GUI display pane
    dfilter_buttons - display filters for repeatable packet analysis
    80211_keys - Wi-Fi SSID and password to decode Wi-Fi encrypted packets

python:

Python progams to create and transform packet captures using dumpcap, tshark, mergecap.

    time_slies.py - capture all packets on a channel over test duration period Y in 
        slices of time X. Examples use Y = 10 minutes, X = 2 minutes.
    mac_traces.py - using output from time_slices.py as input, produces temp files
        that include only desireced mac addresses from each time slice, then merges
        these timeslices into a single packet trace for each mac.
    transform.py - using output from mac_traces.py, produces columnized text files
        with desired packet information

data:

Directory with output from each of the python programs to illustrate what a
completed data pipeline looks like.
