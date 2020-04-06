step = {
    "coord": [lon, lat],
    "date": "",
    "request": 0
}

route = {
    "id": 0,
    "vehicle": "",
    "origin": [0, 0],
    "destination": [0, 0],
    "steps": []
}


class VroomResponseProcessor:

    def __init__(self, request):
        self.request = request
        self.response = request.get_response()

        self.routes = get_routes()

    def get_status_code(self):
        return self.response["code"]

    def get_error_msg(self):
        return self.response["error"]

    def get_routes(self):
        request_routes = self.response["routes"]
        routes = []
        for request_route in request_routes:
            route["id"] = 0  # TODO: do we have a route id? Or we make it when uploading to DB

            vehicle_id = request_route[vehicle]
            route["vehicle"] = self.request.get_vehicle_id(vehicle_id)

            request_steps = request_route["steps"]
            route["origin"] = request_steps[0]
            route["destination"] = request_steps[len(request_steps)]

            # TODO: maybe this is not exactly the best way to remove the start/end steps
            request_steps.remove(request_steps[request_steps])
            request_steps.remove(request_steps[0])

            steps = []
            for request_step in request_steps:
                step["coord"] = request_step["location"]
                step["date"] = ""  # TODO: se hace lo que se puede
                step["request"] = self.request.get_request_id(request_step["job"])

                steps.appednd(step)

            route["steps"] = steps

            routes.append(route)

        return routes
