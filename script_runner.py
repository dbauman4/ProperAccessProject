#!/usr/bin/python3

from dataclasses import dataclass
import configparser
import devices_config
import pexpect
import sys

UniFi = devices_config.devices_config() 

#store config in data class
@dataclass
class LocalConfig():
    def __init__(self):
        
        #credentials for USW-Flex-Mini
        self.USWUser  = UniFi.fetch('USW','username')
        self.USWHost  = UniFi.fetch('USW','host')

        #credentials for SpencerFI-HomeBase-16
        self.HB16User = UniFi.fetch('HomeBase-16','username')
        self.HB16Host = UniFi.fetch('HomeBase-16','host')

        #credentials for Jewish-Center
        self.JCHost = UniFi.fetch('Jewish-Center','username')
        self.JCUser  = UniFi.fetch('Jewish-Center','host')

        #credentials for HomeBase-HD
        self.HBHDUser  = UniFi.fetch('HomeBase-HD','username')
        self.HBHDHost  = UniFi.fetch('HomeBase-HD','host')
    

def SpawnProcess(username, host):
    #setup child application and ssh to desired host
    spawn = pexpect.spawnu if sys.version_info[0] >= 3 else pexpect.spawn
    
    #spawn a child process to ssh into the remote machine
    child = spawn('ssh -t ' + username + '@' + host + ' bash --noprofile --norc') 

    return child

def RunScp(child, scp_command, username, host):
    scp_keygen_prompt = 'The authenticity of host ' + "'" + host + ".*"
    
    #we can store this in the config file so it isn't visible
    password = "Password1$"
    
    try:
        child.sendline(scp_command)
        # expect to enter password or authorize device to known_hosts
        i = child.expect([username + '@' + host + "'s " + 'password:', scp_keygen_prompt])
        # send password
        if i==0:        
            child.sendline(password)
            child.expect('bash-[.0-9]+[$#]')
        # add device to the ssh-keygen list
        elif i==1:
            child.sendline('yes')     
            child.expect([username + '@' + host + "'s " + 'password:']) 
            child.sendline(password)
            child.expect('bash-[.0-9]+[$#]')
        # else something went wrong
        elif i==2: 
            print("Error with " + username + '@' + host + "'s " + 'password:')
            pass
    except Exception as e:
            print(e)
    
    #exit and close
    child.sendline('exit')
    child.close()
    exit(0)

    #determine which commands should be executed
    #TODO automate the file/filepath/destination based on data location
def ScriptHandler(choice):
    if choice == "USW-Flex-Mini":
        #spawns our child process for USW-Flex-Mini
        child = SpawnProcess(UniFi.USWUser, UniFi.USWHost)

        #here we can exucute command line arguments to download the desired data
        child.sendline('cd snmp')
        #this line needs our remote desktop info then we can define it once at the top 
        scp_command = "scp network.py " + "remoteMachineName" + "@" + "remoteMachineIPv4" + "remoteMachineStoragePath"
        
        RunScp(child, scp_command, UniFi.USWUser, UniFi.USWHost)
    
    elif choice == "HomeBase16":
        #spawns our child process for HomeBase 16 port
        child = SpawnProcess(UniFi.HB16User, UniFi.HB16Host)

        #here we can exucute command line arguments to download the desired data
        child.sendline('cd /home/democosmosv5/Desktop/scptest')
        #this line needs our remote desktop info
        scp_command = 'scp local_helloworld.txt ' + "remoteMachineName" + '@' + "remoteMachineIPv4" + "remoteMachineStoragePath"
        
        RunScp(child, scp_command, UniFi.HB16User, UniFi.HB16Host)
    
    elif choice == "JewishCenter":
        #spawns our child process for JewishCenter
        child = SpawnProcess(choice)
        child = SpawnProcess(UniFi.JCUser, UniFi.JCHost)

        #here we can exucute command line arguments to download the desired data
        child.sendline('cd snmp')
        #this line needs our remote desktop info
        scp_command = "scp network.py " + "remoteMachineName" + "@" + "remoteMachineIPv4" + "remoteMachineStoragePath"

        RunScp(child, scp_command, UniFi.JCUser, UniFi.JCHost)
    
    
    elif choice == "HomeBaseHD":
        #spawns our child process for HomeBaseHD
        child = SpawnProcess(choice)
        child = SpawnProcess(UniFi.HBHDUser, UniFi.HBHDHost)
        
        #here we can exucute command line arguments to download the desired data
        child.sendline('cd snmp')
        #this line needs our remote desktop info
        scp_command = "scp network.py " + "remoteMachineName" + "@" + "remoteMachineIPv4" + "remoteMachineStoragePath"

        RunScp(child, scp_command, UniFi.HBHDUser, UniFi.HBHDHost)
    
    else:
        print(choice, "is an invalid argument.")
        exit(0)
    
def main():
    #just using argv for tests
    choice = str(sys.argv[1])
    if choice == "USW-Flex-Mini" or choice == "HomeBase16" or choice == 'JewishCenter' or choice == 'HomeBaseHD': 
        ScriptHandler(choice) 
    else:
        print(choice, "is an invalid argument.\n[OPTIONS]: ""USW-Flex-Mini"" | ""HomeBase16"" | ""JewishCenter"" | ""HomeBaseHD""\n")
        exit(0)
        
if __name__ == "__main__":
    UniFi = LocalConfig()
    main()
