import os
import json

def getLastOutputName():
    next_output_name = 0
    while os.path.exists("movility/outputs/output_%s.json" % next_output_name):
        next_output_name += 1
    return "movility/outputs/output_%s.json"%(next_output_name-1)

def createNewOutput():
    next_output_name = 0
    while os.path.exists("movility/outputs/output_%s.json" % next_output_name):
        next_output_name += 1
    output_data = {
        "solicitudes":[],
        "rutas":[]
    }
    with open("movility/outputs/output_%s.json" % next_output_name, "x") as output_file:
        json.dump(output_data, output_file)
        return "movility/outputs/output_%s.json" % next_output_name

def getLastOutputData():
    with open(getLastOutputName()) as output_file:
        return json.load(output_file)

def setLastOutputData(data):
    with open(getLastOutputName(), 'w') as output_file:
        json.dump(data, output_file)
        return True