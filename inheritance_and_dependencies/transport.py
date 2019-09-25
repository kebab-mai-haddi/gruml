class CarPollutionPermit:
    def __init__(self):
        self.permit = False

    def check_permit(self, year, distance, capacity):
        if year < 2016:
            return False
        from vehicles import Vehicle
        vehicle = Vehicle()
        if vehicle.mileage_calculator(distance, capacity) < 15:
            return True
        return False
