import requests as rest


class VroomRequest:

    DEFAULT_VEHICLE_STATION = [-8.619422214682393, 42.2860253]

    def __init__(self):
        self.vehicle_id_generator = self.get_next_vehicle_id()
        self.job_id_generator = self.get_next_job_id()

        self.shipments = []
        self.vehicles = []

        self.vroom_request = {
            "jobs": [],
            "vehicles": [],
            "shipments": []
        }
    
    def get_request(self):
        return self.vroom_request
    
    def get_response(self):
        # example ={"vehicles":[{"id":0,"start":[2.3526,48.8604],"end":[2.3526,48.8604]}],
        # "jobs":[{"id":0, "location":[2.3691,48.8532]},{"id":1,"location":[2.2911,48.8566]}],"options":{"g":True}}
        res = rest.post("http://localhost:3000/", json=self.vroom_request)
        return res.json()

    def get_vehicle_id(self, vrooom_vehicle_id):
        for vehicle in self.vehicles:
            if vehicle["vroom_vehicle"] == vrooom_vehicle_id:
                return vehicle["db_vehicle"]

    def get_request_id(self, job_id):
        for shipment in self.shipments:
            if shipment["pickup"] == job_id:
                return shipment["request"]
            if shipment["delivery"] == job_id:
                return shipment["request"]

    def get_next_job_id(self):
        next_job_id = 0
        while True:
            yield next_job_id
            next_job_id += 1

    def get_next_vehicle_id(self):
        next_vehicle_id = 0
        while True:
            yield next_vehicle_id
            next_vehicle_id += 1
    
    def add_jobs(self):
        pass
        
    def add_vehicle(self, db_vehicle_id, start=DEFAULT_VEHICLE_STATION, end=DEFAULT_VEHICLE_STATION, profile="car", capacity=8):
        
        vehicle_id = next(self.vehicle_id_generator)
        
        self.vehicles.append({
            "db_vehicle": db_vehicle_id,
            "vroom_vehicle": vehicle_id
        })

        self.vroom_request["vehicles"].append({
            "id": vehicle_id,
            "start": start,  # [lon,lat]
            "end": end,
            "profile": profile,
            "capacity": [capacity]
        })

    def add_shipment(self, db_request_id, pickup_location, delivery_location, pickup_date=None, delivery_date=None, amount=1):
        
        pickup_id = next(self.job_id_generator)
        delivery_id = next(self.job_id_generator)
        
        self.shipments.append({
            "request": db_request_id,
            "pickup": pickup_id,
            "delivery": delivery_id
        })

        pickup_location_array = [float(pickup_location.split(",")[0]), float(pickup_location.split(",")[1])]
        delivery_location_array = [float(delivery_location.split(",")[0]), float(delivery_location.split(",")[1])]

        pickup = {
            "id": pickup_id,
            "location": pickup_location_array
        }
        delivery = {
            "id": delivery_id,
            "location": delivery_location_array
        }

        if pickup_date is not None:
            pickup_date_seconds = pickup_date.timestamp()
            pickup_date_array = [pickup_date_seconds, pickup_date_seconds + 600]  # The pickup can start 10min late max.
            pickup["time_windows"] = [pickup_date_array]

        if delivery_date is not None:
            delivery_date_seconds = delivery_date.timestamp()
            delivery_date_array = [delivery_date_seconds - 600, delivery_date_seconds]  # The delivery can be 10m early
            delivery["time_windows"] = [delivery_date_array]

        self.vroom_request["shipments"].append({
            "amount": [amount],
            "pickup": pickup,
            "delivery": delivery
        })