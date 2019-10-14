from vehicles import Vehicle, Farzi


class CarPollutionPermit(Farzi):
    def __init__(self):
        self.permit = False

    def check_permit(self, year, mileage):
        if year < 2016:
            return False
        if mileage < 15:
            return True
        return False


class BikePollutionPermit:
    def __init__(self):
        self.permit = True

    def check_permit(self, year, mileage):
        if year < 2010:
            self.permit = False
            return False
        if mileage < 40:
            if year > 2016:
                return True
            self.permit = False
            return False
        self.permit = True
        return True
