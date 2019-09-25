class CarPollutionPermit:
    def __init__(self):
        self.permit = False

    def check_permit(self, year, mileage):
        if year < 2016:
            return False
        if mileage < 15:
            return True
        return False
