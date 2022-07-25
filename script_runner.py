#!/usr/bin/python3

import configparser
import pexpect
import sys

#Retrieves data from config file and stores it into a list 
def CosmosConfig(choice):
    dicts = []
    config = configparser.ConfigParser()
    config.read('/home/democosmosv5/Desktop/scptest/cosmos_config.ini')   
    
    #obtain data from config files into dictionary
    local_dict = dict(config.items('localhost'))
    remote_dict = dict(config.items('remotehost'))

    #index 0 == local && index 1 == remote
    if(choice == "remote_scp" or choice == "remote"): 
        dicts.append(local_dict)
        dicts.append(remote_dict)
    #index 0 == remote && index 1 == local
    elif(choice == "local_scp" or choice == "local"):
        dicts.append(remote_dict)
        dicts.append(local_dict)
    else:
        print(choice, "is an invalid argument.\n[OPTIONS]: ""local"" | ""remote"" | ""local_scp"" | ""remote_scp""\n")
        exit(0)
    return dicts

def SpawnProcess(config):
    #setup child application and ssh to desired host
    spawn = pexpect.spawnu if sys.version_info[0] >= 3 else pexpect.spawn
    child = spawn('ssh -t ' + config[1]['username'] + '@' + config[1]['host'] + ' bash --noprofile --norc')
    ssh_keygen_prompt = 'The authenticity of host ' + "'" + config[1]['host'] + ".*"
    
    i = child.expect([config[1]['username'] + '@' + config[1]['host'] + "'s " + 'password:', ssh_keygen_prompt])
    #device is already added to ssh-keygen list
    if i==0: 
        child.sendline(config[1]['password'])
        child.expect('bash-[.0-9]+[$#]')
    if i==1:
         child.sendline('yes')
         child.expect(config[1]['username'] + '@' + config[1]['host'] + "'s " + 'password:')
         child.sendline(config[1]['password'])
         child.expect('bash-[.0-9]+[$#]')
    return child

def RunScp(child,config,scp_command):
    scp_keygen_prompt = 'The authenticity of host ' + "'" + config[0]['host'] + ".*"
    try:
        child.sendline(scp_command)
        # expect to enter password or authorize device to known_hosts
        i = child.expect([config[0]['username'] + '@' + config[0]['host'] + "'s " + 'password:', scp_keygen_prompt])
        # send password
        if i==0:        
            child.sendline(config[0]['password'])
            child.expect('bash-[.0-9]+[$#]')
        # add device to the ssh-keygen list
        elif i==1:
            child.sendline('yes')     
            child.expect([config[0]['username'] + '@' + config[0]['host'] + "'s " + 'password:']) 
            child.sendline(config[0]['password'])
            child.expect('bash-[.0-9]+[$#]')
        # else something went wrong
        elif i==2: 
            print("Error with " + config[0]['username'] + '@' + config[0]['host'] + "'s " + 'password:')
            pass
    except Exception as e:
            print(e)
    
    #exit and close
    child.sendline('exit')
    child.close()
    exit(0)

    #determine which commands should be executed
    #TODO automate the file/filepath/destination
def ScriptHandler(choice,config):
    if choice == "remote_scp":
        child = SpawnProcess(config)
        child.sendline('cd snmp')#/scp_test')
        scp_command = "scp network.py " + config[0]['username'] + "@" + config[0]['host'] + ":/home/democosmosv5/Desktop/scptest"
        RunScp(child,config,scp_command)
    
    elif choice == "local_scp":
        child = SpawnProcess(config)
        child.sendline('cd /home/democosmosv5/Desktop/scptest')
        scp_command = 'scp local_helloworld.txt ' + config[0]['username'] + '@' + config[0]['host'] + ':/home/root/snmp' #/scp_test'
        RunScp(child,config,scp_command)
    
    elif choice == "remote":
        child = SpawnProcess(config)
        
        child.sendline('cd snmp') #/scp_test')
        child.expect('bash-[.0-9]+[$#]')
        child.sendline('ls')
        child.expect('bash-[.0-9]+[$#]')
        
        print(child.before)

        child.sendline('exit')
        child.close()
    
    elif choice == "local":
        child = SpawnProcess(config)
        
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
    config = CosmosConfig(choice)

    if choice == "local" or choice == "remote" or choice == "local_scp" or "remote_scp":
        ScriptHandler(choice,config) 
    else:
        print(choice, "is an invalid argument.\n[OPTIONS]: ""local"" | ""remote"" | ""local_scp"" | ""remote_scp""\n")
        exit(0)
        
if __name__ == "__main__":
    main()
