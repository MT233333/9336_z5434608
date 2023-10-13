import subprocess
import re
import os
import time
import datetime
import csv
import socket

i=0
with open('pj12.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['time','os','network interface',"gps latitude", "gps longitude", "gps accuracy (meters)",'ssid', 'bssid', 'wi-fi standard', "frequency (GHz)", "network channel", "channel width (in mhz)", "rssi (in dbm)", "noise level (dbm)", "public ip address", "network delay (in ms)"])
for i in range(0,31):
    os.popen('chcp 437')

    now = datetime.datetime.now()
    timestamp = int(datetime.datetime.timestamp(now))

    try:
        connected_wifi_delay = subprocess.check_output(["ping", "-n", "1", "cse.unsw.edu.au"],  errors='ignore')
        if m := re.search(r'time=(\d+)ms', connected_wifi_delay):
            Delay= float(m.group(1))
        else:
            Delay = 4000
    except:
        Delay = 4000


    all_wifi = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=Bssid"], encoding='utf-8')

    wifi_lines = re.split(r'\n', all_wifi)

    connected_wifi_info = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], encoding='utf-8')

    if m := re.search(r'BSSID\s+:\s+(.*)', connected_wifi_info):
        current_bssid = m.group(1)

    latitude = None
    longitude = None
    accuracy = None
    ssid = None
    noise = None
    os1 = "Windows 11"
    network = "Intel(R) Wi-Fi 6 AX201 160MHz"
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)



    bssids = []

    for line in wifi_lines:
        if m := re.search(r'SSID\s\d+\s:\s+(.*)', line):
            ssid = m.group(1)
        if n := re.search(r'BSSID\s\d+\s+:\s+(.*)', line):
            bssid = n.group(1)
            if bssid != current_bssid:
                delay = None
                ip1 = None
            if bssid == current_bssid:
                delay = Delay
                ip1 = ip
        if q := re.search(r'Signal\s+:\s+(.*)%', line):
            signal_percentage = float(q.group(1))

            signal = signal_percentage/2 - 100
        if k := re.search(r'type\s+:\s(.*)', line):
            type = k.group(1)
        if o := re.search(r'Band\s+:\s(.*)\sGHz', line):
            frequency = float(o.group(1))
            if frequency == 2.4:
                width = 20
            else:
                width = 40
        if p := re.search(r'Channel\s+:\s+(.*)', line):
            channel = p.group(1)

            bssids.append((ssid, bssid, delay, frequency, channel, type, signal, width, ip1))

    with open('pj12.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        for ssid, bssid, delay, frequency, channel, type, signal, width, ip1 in bssids:
            writer.writerow([timestamp, os1, network, latitude, longitude, accuracy, ssid, bssid, type, frequency, channel, width, signal, noise, ip1, delay])
            
    i=i+1
    print(i)
    time.sleep(20)
print("finished")