from vehicles import Vehicle
from transport import CarPollutionPermit


class Car(Vehicle):
    def __init__(self, model, year=2015, capacity=30):
        self.model = model
        self.year = year
        self.capacity = capacity
        self.pollution_compliance = False

    def pollution_permit(self, distance):
        mileage = self.mileage_calculator(distance, self.capacity)
        car_pollution = CarPollutionPermit()
        self.pollution_compliance = car_pollution.check_permit(
            self.year, mileage)
        print(self.pollution_compliance)

class Bike(Car):
    pass
# car = Car('Indica', year=2017)
# car.pollution_permit(30)
