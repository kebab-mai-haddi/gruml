# from .source_code_to_study import car, transport, vehicles
import sys
# sys.path.insert(0, '/Users/aviralsrivastava/dev/source_code_to_study')
import car
import vehicles
import transport

# def main():
#     tractor_pollution_permit = transport.TractorPollutionPermit()
#     tractor_pollution_permit.fetch_tractor(2018, True)
#     tractor_pesticides = transport.TractorPesticides()
#     tractor_pesticides.fetch_pesticides_permit(11)
#     car_ = car.Car(model='Tesla')
#     car_.pollution_permit(20000)
#     bike = car.Bike('Harley', 2019)
#     bike.pollution_permit(200000)
#     bike.check_farzi()


def main_2():
    print('Inside main_2 func')
    car_ = car.Car(model='Tesla')
    car_.pollution_permit(20000)
    bike = car.Bike('Harley', 2019)
    bike.pollution_permit(200000)
    bike.check_farzi()
    # tractor_pollution_permit = transport.TractorPollutionPermit()
    # tractor_pollution_permit.fetch_tractor(2018, True)
    # tractor_pesticides = transport.TractorPesticides()
    # tractor_pesticides.fetch_pesticides_permit(11)


main_2()
