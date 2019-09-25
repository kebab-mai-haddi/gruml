from vehicles import Vehicle
from transport import CarPollutionPermit


class Car:
    def __init__(self, model, year=2015, capacity=30):
        self.model = model
        self.year = year
        self.capacity = capacity

    def pollution_permit(self, distance):
        car_pollution = CarPollutionPermit()
        return (
            car_pollution.check_permit(self.year, distance, self.capacity)
        )


car = Car('Indica', year=2017)
print(car.pollution_permit(30))
