import json
import pprint
import pandas as pd
from pandas import json_normalize




#loads json into dict objects, usefull for accessing individual objects
def parseTopology():
    with open("topology.json", "r", encoding="utf-8") as f:
        global data
        data = json.loads(f.read())
        global edges
        edges = data["default"]["edges"]
        global vertices
        vertices = data["default"]["vertices"]
        #pprint.pprint(edges)
        #pprint.pprint(vertices)
        #print(data["default"]["edges"][0])

#Prints the charts to the console
def printCharts():
    df = json_normalize(edges)
    print(df)


    df = json_normalize(vertices)
    print(df)




parseTopology()
printCharts()
