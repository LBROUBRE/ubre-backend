import os
import json

WORKSPACE = "/home/sam/Workspace/UBRE/ubre-backend/movility/outputs/"

def getLastOutputName():
    next_output_name = 0
    while os.path.exists(WORKSPACE+"output_%s.json" % next_output_name):
        next_output_name += 1
    return WORKSPACE+"output_%s.json"%(next_output_name-1)

def createNewOutput():
    next_output_name = 0
    while os.path.exists(WORKSPACE+"output_%s.json" % next_output_name):
        next_output_name += 1
    output_data = {
        "solicitudes":[],
        "rutas":[]
    }
    with open(WORKSPACE+"output_%s.json" % next_output_name, "x") as output_file:
        json.dump(output_data, output_file)
        return WORKSPACE+"output_%s.json" % next_output_name

def getLastOutputData():
    with open(getLastOutputName()) as output_file:
        return json.load(output_file)

def setLastOutputData(data):
    with open(getLastOutputName(), 'w') as output_file:
        json.dump(data, output_file)
        return True