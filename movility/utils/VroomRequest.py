class VroomRequest():

    def __init__(self):
        self.vroom_request = {
            "jobs": [],
            "vehicles": [],
            "shipments": []
        }
    
    def get_request(self):
        return self.vroom_request
    
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
        
    def add_vehicle(self, start, end, profile="car", capacity=8):
        self.vroom_request["vehicles"].append({
            "id":self.get_next_vehicle_id(),
            "start":start, # [lon,lat]
            "end":end,
            "profile":profile,
            "capacity":[capacity]
        })

    def add_shipment(self, pickup_location, delivery_location, amount=1):
        self.vroom_request["shipments"].append({
            "amount": [amount],
            "pickup": {
                "id": self.get_next_job_id(),
                "location": pickup_location
            },
            "delivery": {
                "id": self.get_next_job_id(),
                "location": delivery_location
            }
        })