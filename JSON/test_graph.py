import json
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import pylab
import numpy as np
import pprint
import pandas as pd
from pandas import json_normalize

#[edges] -> uplink_Mac, downlinkMac, uplinkPortNumber, rateMbps, uplinkPortNum
#[vertices] -> mac, model, name, type (type can be "DEVICE" or "CLIENT"
def parseTopology():
    with open("topology.json", "r", encoding="utf-8") as f:
        top = json.loads(f.read())
        edges = top["default"]["edges"]
        vertices = top["default"]["vertices"]
        #df_edges = json_normalize(edges)
        #df_vertices = json_normalize(vertices)
        return edges,vertices
        

#[network] -> mac, ip, name
#[radios] na/ng -> maxPower, maxSpeedMegabitsPerSecond
#[appInfo] -> apCount,switchCount,clientCount,wiredClients, wirelessClients, throughput
#[lastSpeedTest] -> downloadSpeed, ping, runDate, uploadSpeed
#[portTable] -> fullDuplex, ifname, name, throughputRx, throughputTx, type, usageRx, usageTx
def parseBasicInfo():
    with open("basicInfo.json","r", encoding="utf-8") as f:
        basicInfo = json.loads(f.read())
        network = basicInfo["detail"]["deviceList"]["network"]
        radios = basicInfo["detail"]["deviceList"]["network"]["radios"]
        appInfo = basicInfo["detail"]["apps"]["info"]
        lastSpeedTest = basicInfo["detail"]["apps"]["lastSpeedTest"]
        portTable = basicInfo["detail"]["apps"]["info"]["port_table"]

#[default] -> ip, mac, model, type, bytes-d, tx_bytes-d, rx_bytes-d, bytes-r, connect_request_ip
#[uplink] -> bytes, tx_bytes, rx_bytes, tx_packets, rx_packets
#[downlink_table] -> mac, port_idx, speed, full_duplex
#[radio_table] -> radio, name, channel, radio_caps, radio_capts2, max_txpower, min_txpower, channel
#[port_table] -> media, mac, ifname, port_poe, poe_caps, speed_caps, speed, port_idx
#[ethernet_table] ->mac, num_port, name
#[last_uplink] -> uplink_mac, uplink_device, uplink_remote_port, port_idx, type

def parseDevices():
    with open("devices.json", "r", encoding="utf-8") as f:
        devices = json.loads(f.read())
        default = devices[0]["default"]
        uplink = devices[0]["default"]["uplink"]
        downlink_table = devices[0]["default"]["downlink_table"]
        radio_table = devices[0]["default"]["radio_table"]
        port_table = devices[0]["default"]["port_table"]
        ethernet_table = devices[0]["default"]["ethernet_table"]
        last_uplink = devices[0]["default"]["last_uplink"]
        return default
        

#[port_table] -> name, rx_broadcast, rx_bytes, rx_dropped, rx_errors, rx_packets, rx_multicast, 
#tx_broadcast, tx_bytes, tx_multicast, tx_dropped, tx_packets, port_idx, media, speed_caps, 
#is_uplink, full_duplex
def parseNetworkSysconf():
    with open("network_sysconf_11-07-2022 (1).json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
        #print(len(data["device"]))
        print(len(data["device"]["0"]["port_table"]))
        port_table = []
        for x in range(0,len(data["device"])-1):
            for y in range(0,len(data["device"][str(x)]["port_table"])-1):
                if len(data["device"][str(x)]["port_table"]) != 0:
                    port_table.append(data["device"][str(x)]["port_table"][str(y)]) 
                
    
    printCharts(port_table)
    
#bar chart in future using basic info
#y (number of bytes) rx & tx usage, color coded, diff lines
#x mac/ip of device
def barChart():
    #print the device types and ip 
    devices_default = parseDevices()
    for i in range(len(devices_default)):
        print(devices_default[i]["type"] + " : "+ devices_default[i]["mac"])
        #if("downlink_table" in devices_default[i]):
        #    print("downlink_table in "+ str(i))

    edges, verticies = parseTopology()

    connections = {}
    clients = []
    devices = []
    totalclients = 0
    totaldevice = 0
    for i in range(len(verticies)):
        print(verticies[i]["type"] + " : " + verticies[i]["mac"])
        #connections.update({verticies[i]["mac"]:[]})
        if(verticies[i]["type"]=="DEVICE"):
            devices.append(verticies[i]["mac"])
            connections.update({verticies[i]["mac"]:[]})
            totaldevice+=1
        else:
            clients.append(verticies[i]["mac"])
            totalclients+=1
    print("total clients: "+str(totalclients)+" total devices: "+str(totaldevice) + "\n")

    for i in range(len(edges)):
        print(edges[i]["type"] + " : " + edges[i]["downlinkMac"] + " -> " + edges[i]["uplinkMac"])
        if(edges[i]["uplinkMac"] in connections):
            connections[edges[i]["uplinkMac"]].append(edges[i]["downlinkMac"])

    for k,v in connections.items():
        print(k)
        if(len(v)!=0):
            for y in range(len(v)):
                print("\t"+str(connections[k][y]))
        else:
            print("\tN/A")
    
    print("Clients: "+str(clients))
    print("Devices: "+str(devices))

    for i in range(len(devices_default)):
        #print(i)
        if devices_default[i]["mac"] in devices:
            print(i)
    
def printCharts(port_table = []):
    df = json_normalize(port_table)
    sns.kdeplot(df['rx_bytes'])
    #df.plot(kind = 'line',
    #         x = 'rx_bytes',
    #         y = 'tx_bytes',
    #         color = 'blue')
    plt.title('Rx Density')
    plt.savefig('Rx_density.png') 
    plt.show()
    print(df)
    #df = json_normalize(vertices)
    #print(df)

def main():
    barChart()

main()
#parseNetworkSysconf()
#printCharts()
