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

        self.routes = self.get_routes()

    def get_status_code(self):
        return self.response["code"]

    def get_error_msg(self):
        return self.response["error"]

    def get_routes(self):
        print(self.response)
        request_routes = self.response["routes"]
        routes = []
        for request_route in request_routes:

            vehicle_id = request_route["vehicle"]
            route["vehiculo"] = self.request.get_vehicle_id(vehicle_id)

            request_steps = request_route["steps"]
            route["origen"] = "%f, %f" % (request_steps[0]["location"][0], request_steps[0]["location"][1])
            route["destino"] = "%f, %f" % (request_steps[-1]["location"][0], request_steps[-1]["location"][1])

            # TODO: maybe this is not exactly the best way to remove the start/end steps
            request_steps.remove(request_steps[-1])
            request_steps.remove(request_steps[0])

            steps = []
            for request_step in request_steps:
                step["coordenadas"] = "%f, %f" % (request_step["location"][0], request_step["location"][1])
                step["fechaHora"] = "2020-04-06 18:00:31+00:00"  # TODO: se hace lo que se puede
                step["solicitudes"] = self.request.get_request_id(request_step["job"])

                steps.append(step)

            route["paradas"] = steps

            routes.append(route)

        return routes
