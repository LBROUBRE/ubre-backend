step = {
    "coordenadas": [0, 0],
    "fechaHora": "",
    "solicitudes": 0
}

route = {
    "vehiculo": "",
    "origen": [0, 0],
    "destino": [0, 0],
    "paradas": []
}


class VroomResponseProcessor:

    def __init__(self, request):
        self.request = request
        self.response = request.get_response()

    def get_status_code(self):
        return self.response["code"]

    def get_error_msg(self):
        return self.response["error"]

    def get_routes(self):
        request_routes = self.response["routes"]
        routes = []
        for request_route in request_routes:
            route = dict()

            vehicle_id = request_route["vehicle"]
            route["vehiculo"] = self.request.get_vehicle_id(vehicle_id)
            route["geometry"] = request_route["geometry"]

            request_steps = request_route["steps"]
            route["origen"] = "%f, %f" % (request_steps[0]["location"][0], request_steps[0]["location"][1])
            route["destino"] = "%f, %f" % (request_steps[-1]["location"][0], request_steps[-1]["location"][1])

            request_steps.remove(request_steps[-1])
            request_steps.remove(request_steps[0])

            if "unassigned" in self.response:
                for request_unassigned in self.response["unassigned"]:  # We will set the unassigned request to rejected
                    request_id = self.request.get_request_id(request_unassigned["id"])
                    import requests as rest
                    json = {
                        "estado": 'R'
                    }
                    res = rest.put("http://127.0.0.1:8000/movility/requests/%i" % request_id, json=json)
                    print(res)

            steps = []
            for request_step in request_steps:
                from datetime import datetime
                new_step = dict()
                new_step["parada"] = self.request.get_stop_id(request_step["job"])
                date = datetime.fromtimestamp(request_step["arrival"])
                new_step["fechaHora"] = date.strftime('%Y-%m-%dT%H:%M:%SZ')
                new_step["solicitudes"] = self.request.get_request_id(request_step["job"])

                steps.append(new_step)

            route["paradas"] = steps

            routes.append(route)

        return routes
