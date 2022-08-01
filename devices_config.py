import sys

class inifile():
    def __init__(self,filename):
        self.fname = filename
        self.sections = {}

    def load(self):
        with open(self.fname,'r') as inf:
            section=None
            for line in inf.readlines():
                if line[0]==';':
                    continue
                elif line[0]=='[':
                    section = line[1:-2]
                else:
                    k,v = line[:-1].split('=')
                    if not section in self.sections:
                        self.sections[section]={}
                    self.sections[section][k]=v

    def save(self):
        with open(self.fname,'w') as ouf:
            if None in self.sections:
                for k,v in self.sections[None].items():
                    ouf.write('{}={}\n'.format(k,v))
            for section in self.sections:
                if section == None:
                    continue
                ouf.write('[{}]\n'.format(section))
                for k,v in self.sections[section].items():
                    ouf.write('{}={}\n'.format(k,v))

    def fetch(self,section,key):
        return self.sections[section][key]
    
    def set(self,section,key,value):
        self.sections[section][key]=value
    
    def addsection(self,section):
        self.sections[section] = {}
    
    def getsection(self,section):
        return self.sections[section]

class devices_config():
    def __init__(self,filename='/home/democosmosv5/Desktop/scptest/devices_config.ini'):
        self.inifile = inifile(filename)
        try:
            self.inifile.load()
        except: #no config file. Make some defaults.
            sys.stderr.write('couldn\'t load config\ngenerated default devices_config.ini\n')
            self.reset()
        self.fetch=self.inifile.fetch
        self.set=self.inifile.set
        self.save=self.inifile.save

    def reset(self):
            
            self.inifile.addsection('USW')
            USW = self.inifile.getsection('USW')
            USW['username']='USW-Flex-Mini'
            USW['host']='192.168.1.46'
            
            self.inifile.addsection('HomeBase-16')
            HomeBase16 = self.inifile.getsection('HomeBase-16')
            HomeBase16['username']='SpencerFi-HomeBase-16-Port-US.6.2.14'
            HomeBase16['host']='192.168.1.205'
            
            self.inifile.addsection('Jewish-Center')
            JC = self.inifile.getsection('Jewish-Center')
            JC['username'] = 'JewishCenter-BZ.6.0.21'
            JC['host'] = '192.168.1.66'
            
            self.inifile.addsection('HomeBase-HD')
            HBHD = self.inifile.getsection('HomeBase-HD')
            HBHD['username'] = 'HomeBaseHDWiFiAccessPoint-BZ.6.0.21'
            HBHD['host'] = '192.168.1.208'
            self.inifile.save()