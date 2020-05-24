import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl


class SteakDoneness(object):
    def __init__(self):
        self.thickness = ctrl.Antecedent(np.arange(0.5, 5.5, 0.5), 'thickness')
        self.temperature = ctrl.Antecedent(np.arange(50, 85, 5), 'temperature')
        self.frying_time = ctrl.Antecedent(np.arange(2, 18, 2), 'frying time')
        self.doneness = ctrl.Consequent(np.arange(0, 11, 1), 'doneness')

        self.thickness['thin'] = fuzz.trapmf(self.thickness.universe, [0.5, 0.5, 1, 1.5])
        self.thickness['medium'] = fuzz.trapmf(self.thickness.universe, [1, 2, 3.5, 4])
        self.thickness['thick'] = fuzz.trapmf(self.thickness.universe, [3.5, 4, 5, 5])

        self.temperature['low'] = fuzz.trapmf(self.temperature.universe, [50, 50, 55, 60])
        self.temperature['medium'] = fuzz.trapmf(self.temperature.universe, [55, 60, 70, 75])
        self.temperature['high'] = fuzz.trapmf(self.temperature.universe, [70, 75, 80, 80])

        self.frying_time['short'] = fuzz.trapmf(self.frying_time.universe, [2, 2, 4, 6])
        self.frying_time['medium'] = fuzz.trapmf(self.frying_time.universe, [4, 6, 10, 12])
        self.frying_time['long'] = fuzz.trapmf(self.frying_time.universe, [10, 12, 14, 16])
        self.frying_time['very long'] = fuzz.trapmf(self.frying_time.universe, [12, 14, 16, 16])

        self.doneness['rare'] = fuzz.trimf(self.doneness.universe, [0, 1, 2])
        self.doneness['medium rare'] = fuzz.trimf(self.doneness.universe, [1, 3, 4])
        self.doneness['medium'] = fuzz.trimf(self.doneness.universe, [3, 5, 7])
        self.doneness['medium well'] = fuzz.trimf(self.doneness.universe, [6, 7, 9])
        self.doneness['well'] = fuzz.trimf(self.doneness.universe, [8, 9, 10])

        self.rules = [
            ctrl.Rule((self.thickness['thin'] | self.thickness['medium']) & self.temperature['low'] &
                      self.frying_time['short'], self.doneness['rare']),

            ctrl.Rule(self.thickness['thick'] & (self.temperature['low'] | self.temperature['medium']) &
                      (self.frying_time['short'] | self.frying_time['medium']), self.doneness['rare']),

            ctrl.Rule(self.thickness['thin'] & (self.temperature['medium'] | self.temperature['high']) &
                      (self.frying_time['short'] | self.frying_time['medium']), self.doneness['medium rare']),

            ctrl.Rule((self.thickness['thin'] | self.thickness['medium']) & self.temperature['low'] &
                      self.frying_time['medium'], self.doneness['medium rare']),

            ctrl.Rule(self.thickness['thick'] & self.temperature['high'] &
                      self.frying_time['short'], self.doneness['medium rare']),

            ctrl.Rule(self.thickness['medium'] & (self.temperature['medium'] | self.temperature['high']) &
                      (self.frying_time['short'] | self.frying_time['medium']), self.doneness['medium rare']),

            ctrl.Rule(self.thickness['thick'] & self.temperature['low'] &
                      (self.frying_time['long'] | self.frying_time['very long']), self.doneness['medium rare']),

            ctrl.Rule(self.thickness['thick'] & (self.temperature['medium'] | self.temperature['high']) &
                      self.frying_time['medium'], self.doneness['medium rare']),

            ctrl.Rule(self.thickness['thin'] & self.temperature['medium'] &
                      self.frying_time['long'], self.doneness['medium']),

            ctrl.Rule((self.thickness['medium'] | self.thickness['thick']) & self.temperature['medium'] &
                      self.frying_time['long'], self.doneness['medium']),

            ctrl.Rule((self.thickness['thin'] | self.thickness['medium']) & self.temperature['low'] &
                      self.frying_time['long'], self.doneness['medium']),

            ctrl.Rule(self.thickness['thin'] & self.temperature['high'] &
                      (self.frying_time['medium'] | self.frying_time['long']), self.doneness['medium well']),

            ctrl.Rule(self.thickness['medium'] & (self.temperature['medium'] | self.temperature['high']) &
                      self.frying_time['long'], self.doneness['medium well']),

            ctrl.Rule(self.thickness['thick'] & self.temperature['high'] &
                      self.frying_time['long'], self.doneness['medium well']),

            ctrl.Rule(self.frying_time['very long'], self.doneness['well'])
        ]

    def view_functions(self):
        self.thickness.view()
        self.temperature.view()
        self.frying_time.view()
        self.doneness.view()

    def simulate(self):
        return ctrl.ControlSystemSimulation(ctrl.ControlSystem(self.rules))


if __name__ == '__main__':
    steak_doneness = SteakDoneness()
    steak_doneness.view_functions()

    simulation = steak_doneness.simulate()
    simulation.input['thickness'] = float(input("Thickness (cm)[0.5-5]: "))
    simulation.input['temperature'] = int(input("Temperature (°C)[50-80]: "))
    simulation.input['frying time'] = int(input("Frying time (min)[2-16]: "))
    simulation.compute()

    print("Steak doneness: ", simulation.output['doneness'])
    steak_doneness.doneness.view(sim=simulation)
