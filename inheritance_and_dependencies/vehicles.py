class Vehicle:
    def __init__(self, usage='domestic'):
        self.usage = usage

    def mileage_calculator(self, distance, capacity):
        self.mileage = distance/capacity
        return self.mileage
