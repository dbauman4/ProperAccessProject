#!/usr/bin/python3

from dataclasses import dataclass
import configparser
import cosmos_config
import pexpect
import sys

cosmos = cosmos_config.cosmos_config() 

#store config in data class
@dataclass
class LocalConfig():
    def __init__(self):
        self.localUser  = cosmos.fetch('localhost','username')
        self.localHost  = cosmos.fetch('localhost','host')
        self.localPass  = cosmos.fetch('localhost','password')
        self.remoteUser = cosmos.fetch('remotehost','username')
        self.remoteHost = cosmos.fetch('remotehost','host')
        self.remotePass = cosmos.fetch('remotehost','password')
    
    #TODO error handle if choice is neither
def SpawnProcess(choice):
    #setup child application and ssh to desired host
    spawn = pexpect.spawnu if sys.version_info[0] >= 3 else pexpect.spawn
    
    if(choice == "remotehost_scp" or choice == "remotehost"):
        #spawn a child process to ssh into the remote machine
        child = spawn('ssh -t ' + config.remoteUser + '@' + config.remoteHost + ' bash --noprofile --norc') 
        ssh_keygen_prompt = 'The authenticity of host ' + "'" + config.remoteHost + ".*"
        Authenticate(child, config.remoteUser, config.remoteHost, config.remotePass, ssh_keygen_prompt)
        return child
    if(choice == "localhost_scp" or choice == "localhost"):
        #spawn a child process to ssh into the local machine
        child = spawn('ssh -t ' + config.localUser + '@' + config.localHost + ' bash --noprofile --norc')            
        ssh_keygen_prompt = 'The authenticity of host ' + "'" + config.localHost + ".*"
        Authenticate(child, config.localUser, config.localHost, config.localPass, ssh_keygen_prompt)
        return child

def Authenticate(child, username, host, password, ssh_keygen_prompt):
    i = child.expect( [username + '@' + host + "'s " + 'password:', ssh_keygen_prompt])
    #device is already added to ssh-keygen list
    if i==0: 
        child.sendline(password)
        child.expect('bash-[.0-9]+[$#]')
    #device is not added to ssh-keygen list
    if i==1:
         child.sendline('yes')
         child.expect(username + '@' + host + "'s " + 'password:')
         child.sendline(password)
         child.expect('bash-[.0-9]+[$#]')
    #return child

def RunScp(child,scp_command, username,host, password):
    scp_keygen_prompt = 'The authenticity of host ' + "'" + host + ".*"
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
    #TODO automate the file/filepath/destination
def ScriptHandler(choice):
    if choice == "remotehost_scp":
        child = SpawnProcess(choice)
        child.sendline('cd snmp')
        scp_command = "scp network.py " + config.localUser + "@" + config.localHost + ":/home/democosmosv5/Desktop/scptest"
        RunScp(child,scp_command,config.localUser, config.localHost, config.localPass)
    
    elif choice == "localhost_scp":
        child = SpawnProcess(choice)
        child.sendline('cd /home/democosmosv5/Desktop/scptest')
        scp_command = 'scp local_helloworld.txt ' + config.remoteUser + '@' + config.remoteHost + ':/root/snmp'
        RunScp(child,scp_command,config.remoteUser, config.remoteHost, config.remotePass)
    
    elif choice == "remotehost":
        child = SpawnProcess(choice)
        
        child.sendline('cd snmp') 
        child.expect('bash-[.0-9]+[$#]')
        child.sendline('ls')
        child.expect('bash-[.0-9]+[$#]')
        
        print(child.before)

        child.sendline('exit')
        child.close()
    
    elif choice == "localhost":
        child = SpawnProcess(choice)
        child.sendline('cd /home/democosmosv5/Desktop/scptest')
        child.expect('bash-[.0-9]+[$#]')
        child.sendline('ls')
        child.expect('bash-[.0-9]+[$#]')
        print(child.before)
        
        child.sendline('exit')
        child.close()   
    else:
        print(choice, "is an invalid argument.")
        exit(0)
    
def main():
    choice = str(sys.argv[1])
    
    if choice == "localhost" or choice == "remotehost" or choice == 'localhost_scp' or choice == 'remotehost_scp': 
        ScriptHandler(choice) 
    else:
        print(choice, "is an invalid argument.\n[OPTIONS]: ""local"" | ""remote"" | ""localhost_scp"" | ""remotehost_scp""\n")
        exit(0)
        
if __name__ == "__main__":
    config = LocalConfig()#cosmos_config()
    main()