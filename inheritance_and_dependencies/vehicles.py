class Vehicle:
    def __init__(self, usage='domestic'):
        self.usage = usage

    def mileage_calculator(self, distance, capacity):
        self.mileage = distance/capacity
        return self.mileage


class Farzi:
    def __init__(self, farzi):
        self.farzi = farzi

    def check_farzi(self, name):
        if name == self.farzi:
            return True
        return False
