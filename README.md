# ProperAccessProject
1. Decide on programming language
2. Decide on the overall program structure
3. Find common filepath of topology.json
4. Learn how to parse JSON objects
5. Figure out best hashmap design
6. Store parsed JSON objects into hashmap
7. Implement a function to repeatedly compare (every 5min or something) current devices on the network with the hashmap to keep it updated
8. Design criteria for when to move a device to a different ip/channel

USW-Flex-Mini:192.168.1.46 / SpencerFi-HomeBase:192,168.1.1 don't open on debug menu
**Devices for config (shouldn't need passwords if run on remote desktop)** 
```
USW-Flex-Mini IP: 192.168.1.46
SpencerFi-HomeBase 16-Port IP: 192.168.1.205 
SpencerFi-HomeBase IP: 192.168.1.1
Jewish Center IP: 192.168.1.66
Home Base HD WiFi Acess Point IP: 192.168.1.208
```

**using script_runner.py**
We'll import it into our main.py or whatever we choose to name it
Then we just need to call ScriptHandler(device_name) in our program to retrieve files (still working on what we'll pass to it, but I'm thinking just device name)
