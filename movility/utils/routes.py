
def name_to_coordinates(search_string, alldata=False):
    from OSMPythonTools.nominatim import Nominatim
    nominatim = Nominatim()
    response = nominatim.query(search_string).toJSON() # json["matches_number"]["info_parameter"]
    if (alldata): return response
    else: return str(response[0]["lat"]) + ", " + str(response[0]["lon"])