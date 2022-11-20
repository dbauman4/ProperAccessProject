import socket
import sys
import numpy as np
import random
import time
import bitstring
import binascii
import datetime
#from datetime import datetime
from random import randint
from bitarray import bitarray

count = 0 # global count for demo health and status collect button

#########################################Method Declarations#################################

#generates data for POSVEL command
def POSVEL():
    POSX = randint(0,200)
    POSY = randint(0,200)
    POSZ = randint(0,200)
    VELX = randint(0,200)
    VELY = randint(0,200)
    VELZ = randint(0,200)
    filler = bytearray(b'\x00\x00\x00')
    packet1 = bytearray(b'\x00\x00\x00\x1C\x00\x00\x00\x04\x00\x00\x00')
    packet1.append(POSX) #appends random value of POSX to byte array
    packet1.extend(filler) #fills to keep 4byte blocks 
    packet1.append(POSY)
    packet1.extend(filler)
    packet1.append(POSZ)
    packet1.extend(filler)
    packet1.append(VELX)
    packet1.extend(filler)
    packet1.append(VELY)
    packet1.extend(filler)
    packet1.append(VELZ)
    return packet1

#converts epoch time in seconds to hex
def epoch_to_hex():
    now_tm = (datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    time_array = time.strptime(now_tm, '%Y%m%d%H%M%S')
    stamp_tm = int(time.mktime(time_array))
    return_tm = hex(stamp_tm)[2:]
    return return_tm
    
#creates a CCSDS packet header for health status collect in cosmos telemtry viewer
def CCSDS_HEADER():  
  #PARAMETER    CCSDSVER        0   3  UINT  0     0   0 "CCSDS primary header version number"
  #PARAMETER    CCSDSTYPE       3   1  UINT  1     1   1 "CCSDS primary header packet type"
  #PARAMETER    CCSDSSHF        4   1  UINT  0     0   0 "CCSDS primary header secondary header flag"
  #ID_PARAMETER CCSDSAPID       5  11  UINT  0  2047 999 "CCSDS primary header application id"
  #PARAMETER    CCSDSSEQFLAGS  16   2  UINT  3     3   3 "CCSDS primary header sequence flags"
  #PARAMETER    CCSDSSEQCNT    18  14  UINT  0 16383   0 "CCSDS primary header sequence count"
  #OVERFLOW TRUNCATE
  #PARAMETER    CCSDSLENGTH    32  16  UINT MIN MAX 12 "CCSDS primary header packet length"
  #ID_PARAMETER PKTID          48  16  UINT MIN MAX <%= id %> "Packet id"

  #13E7C0000020 60F5CF0E 017AC030D035 0001 0009 0008000000FF 40A0000000000001
  #13E7C0000020 60F203D7 017AB15F0060 0001 0002 003E00000063 40A0000000000001                              
                                                             #20 
    CCSDS = bytearray(b'\x13\xe7\xc0\x00\x00\x1e')  #(b'\x00\x00\x00\x21\x77\xCC\x00\x00\x24')
   # print('bytearray:',CCSDS)

    epoch = epoch_to_hex() #convert epoch time in seconds to hex
    #print('epoch:',epoch)
    epoch = bytes.fromhex(epoch)#store epoch time in byte array to extend it to ccsds packet
    print('epoch:',epoch)
    CCSDS.extend(epoch)

    curr_milli = int(round(time.time() * 1000)) #retrieve current time in milliseconds
    bytes_val = curr_milli.to_bytes(6,'big')
    print('bytes_val:',bytes_val)


    temp = bytearray(b'\x00\x00\x00\x00')

    for i in range(4):
        temp[i] = bytes_val[i]
    
    print('temp:',temp)
    CCSDS.extend(temp)

    #CCSDS.extend(bytes_val)
    CCSDS.extend(b'\x00\x01') #packet id doesn't change
    return CCSDS #returns CCSDS packet header for health status collect

######################################Start of TCP SERVER##############################################

#Creates TCP/IP socket
             #AF_INET = IPV4 as INT  #SOCK_STREAM = TCP 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the socket to the port
server_address = ('127.0.0.1', 8888)

print(sys.stderr, 'starting up on %s port %s' % server_address)

#bind = associate socket w/ server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print(sys.stderr, 'waiting for a connection')

    connection, client_address = sock.accept()
    try:
        print(sys.stderr, 'connection from %d', client_address)
        
        #packet format:
                               #length            ID             Temp           Temp1
        #packet = b'\x00\x00\x00\x0C\x00\x00\x00\x03\x00\x00\x00\x33\x00\x00\x00\x44'
        
        #packet1 format: 
                               #length            ID             POSX            POSY            POSZ            VELX           VELY            VELZ
        #packet1 = b'\x00\x00\x00\x1C\x00\x00\x00\x04\x00\x00\x00\x07\x00\x00\x00\x06\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04'
                          
        while True:
            # Receive the data and retransmit it
            data = connection.recv(4096)
            print(sys.stderr, 'received:', data)
 
                    #incoming temps collect command
            if data == b'\x00\x00\x00\x05\x01\x00\x00\x00\x00':
                print(sys.stderr, 'sending data back to the client')
                
                #random values assigned to temps for demo
                Temp = randint(0,100)
                Temp1 = randint(0,65)
                
                #store telemetry packet into byte array to append random temp values
                                                   
                packet = bytearray(b'\x00\x00\x00\x16\x00\x00\x00\x03\x00\x00\x00')
                packet.append(Temp) #append random number representing temperature between 0-25 to packet
                packet.append(0) 
                packet.append(0) 
                packet.append(0)
                packet.append(Temp1)
                print('packet:',packet)
                
                #######################
                epoch = epoch_to_hex()
                epoch = bytes.fromhex(epoch)
                print('epoch:',epoch)
                packet.extend(epoch)
                
                curr_milli = int(round(time.time() * 1000))
                print('curr_milli:',curr_milli)
                bytes_val = curr_milli.to_bytes(6,'big')
                #print('bytes_val:',bytes_val)
                
                temp = bytearray(b'\x00\x00\x00\x00')
                
                for i in range(4):
                    temp[i] = bytes_val[i]

                packet.extend(temp)
                #packet.extend(bytes_val)
                
                packet.append(0)
                packet.append(1)
                print('packet:',packet)
                connection.sendall(packet)

            elif data == b'\x00\x00\x00\x05\x02': #incoming POSVEL command
                print(sys.stderr, 'sending data back to the client')
                packetPOSVEL = POSVEL()
                #print('packet1:', POSVEL())
                print('packetPOSVEL', packetPOSVEL)
                connection.sendall(packetPOSVEL)
            
            elif data == b'\x00\x00\x00\x05\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': #incoming FLTCMD 
                print(sys.stderr, 'sending data back to the client')
                packetFLT = b'\x00\x00\x00\x0C\x00\x00\x00\x05\x00\x00\x04\x02\x00\x00\x04\x06'
                print('packetFLT', packetFLT)
                connection.sendall(packetFLT)
                                                                   #40  #a0  tlm viewer HS collect
                                                        #ID        #3f  #80  command sender collect
            elif data == b'\x13\xe7\xc0\x00\x00\x0c\x00\x01\x00\x00\x40\xa0\x00\x00\xab\x00\x00\x00\x00':#Calls a COLLECT on BOB Health and Status
                print(sys.stderr, 'sending data back to client')
                count+=1
#18      
                CCSDS = CCSDS_HEADER()
                print('CCSDS:',CCSDS)
     #bob health status tlm after CCSD packet header           
                health_status = bytearray()
                health_status.append(0)
                health_status.append(count) 
                Temp1 = randint(0,100)
                Temp2 = randint(0,255)
                print('Temp1:',Temp1)
                print('Temp2:',Temp2)
   
                health_status.append(0)
                health_status.append(Temp1)
                health_status.extend(b'\x00\x00\x00')
                health_status.append(Temp2)
                health_status.extend(b'\x40\xa0\x00\x00\x00\x00\x00\x01')
                #health_status.extend(filler)
                #health_status.extend(b'\x01')
                print('health_status:',health_status)
                CCSDS.extend(health_status)
                print('completed packet:',CCSDS)
                connection.sendall(CCSDS)

            else:
                #print(sys.stderr, 'Neither condition met')
                print(sys.stderr, 'no more data from', client_address)
                break
     
    finally:
        # Clean up the connection
        connection.close()