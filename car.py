from vehicles import Vehicle, Farzi
from transport import CarPollutionPermit, BikePollutionPermit


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


class Bike(Vehicle):
    def __init__(self, model, year):
        self.model = model
        self.year = year
        self.capacity = 100
        self.pollution_compliance = True
        self.car_pollution_permit = CarPollutionPermit()

    def pollution_permit(self, distance):
        mileage = self.mileage_calculator(distance, self.capacity)
        bike_pollution = BikePollutionPermit()
        self.pollution_compliance = bike_pollution.check_permit(
            self.year, mileage)
        print(self.pollution_compliance)

    def check_farzi(self, bike='farzi'):
        farzi = Farzi(bike)
        print(farzi.check_farzi(bike))


# car = Car('Indica', year=2017)
# car.pollution_permit(30)