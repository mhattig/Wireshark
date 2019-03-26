This repository provides Wireshark config files and python programs that use Wireshark tools.
A data sample is included. Subdirectories in the repository are:

    config
    python

The config directory contains wireshark configuration files. These files are to be copied
into the user's ~/.config/wireshark directory. The ~/.config/wireshark directory is 
created as part of the installation of Wireshark 2.6.6. 

    preferences - defines wireshark window pane layout and columns in the display pane
    colorfilters - associates colors with protocol fields and field values to create 
        visual patterns of packet flows in Wireshark GUI display pane
    dfilter_buttons - display filters for repeatable packet analysis
    80211_keys - Wi-Fi SSID and password to decode Wi-Fi encrypted packets

The python directory contains Python 2.7 progams to create and transform packet captures 
using dumpcap, tshark, mergecap.

    time_slies.py - capture all packets on a channel over test duration period Y in 
        slices of time X. Examples use Y = 10 minutes, X = 2 minutes, 2 mac addrs.
    mac_traces.py - using output from time_slices.py as input, produces temp files
        that include only desired mac addresses from each time slice, then merges
        these timeslices into a single packet trace for each mac.
    transform.py - using output from mac_traces.py, produces columnized text files
        with desired packet information

The data.zip file is a sample dataset from the python programs for a 10 minute test
duration, 2 minute time slices, and 1 MAC address. A capture filter was used to 
reduce the size of the packet capture files.
