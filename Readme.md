This repository provides Wireshark config files and python programs that use Wireshark tools.

Wireshark config files should be downloaded into the OSX directory of <HOME>/.config/wireshark or equivalent for Windows or Linux. These files configure the Wireshark GUI interface. 

Wireshark Config files:

    colorfilters - mark Wi-Fi packets of intereset a particular color in the Wireshark GUI. Provides 
        color patterns of things like Wi-Fi Association, DHCP, DNS, TCP connection/disconnect. Looking
        at packets based purely on text in protocol fields is highly error prone.
    preferences - predefined display filters to only display particular packets (e.g. WiFi 4-way 
        handshake, DHCP, DNS, TCP).  Must set AP an STA Mac address in the file. Can be done 
        with an Wireshark GUI or with text editor (but be careful). Change XX:XX:XX:XX:XX:XX 
        and YY:YY:YY:YY:YY:YY to MAC address of STA and MAC address of AP.

Python programs:

    get_packet_capture_files.py - capture all packets on a channel over a period of hours 
        in 20 minute chunks. Capture files get too big for Wireshark to load after about 20 minutes
        in most environments. 
    extract_packets.py - take output from get_packet_capture_file.py as input to extract packets 
        for a single MAC from all the packet captures, splice them all together to create a single 
        file for one MAC address over an extended period of time (e.g. days, weeks).
