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

            print("-------------------------------\n")
            print(request_route)
            print("\n-------------------------------")

            vehicle_id = request_route["vehicle"]
            route["vehiculo"] = self.request.get_vehicle_id(vehicle_id)

            request_steps = request_route["steps"]
            route["origen"] = "%f, %f" % (request_steps[0]["location"][0], request_steps[0]["location"][1])
            route["destino"] = "%f, %f" % (request_steps[-1]["location"][0], request_steps[-1]["location"][1])

            # TODO: maybe this is not exactly the best way to remove the start/end steps, can we make a loop? (worth)
            request_steps.remove(request_steps[-1])
            request_steps.remove(request_steps[0])

            steps = []
            for request_step in request_steps:
                from datetime import datetime
                new_step = dict()
                new_step["coordenadas"] = "%f, %f" % (request_step["location"][0], request_step["location"][1])
                date = datetime.fromtimestamp(request_step["arrival"])
                new_step["fechaHora"] = date.strftime('%Y-%m-%dT%H:%M:%SZ')
                new_step["solicitudes"] = self.request.get_request_id(request_step["job"])

                steps.append(new_step)

            route["paradas"] = steps

            routes.append(route)

        return routes
