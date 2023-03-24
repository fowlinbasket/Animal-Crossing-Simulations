'''
The code in this file uses many ideas from GitHub user Treeki's work, 
which can be found in https://gist.github.com/Treeki/85be14d297c80c8b3c0a76375743325b.
'''

import random
import matplotlib.pyplot as plt
import os
import numpy as np

DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
TIMES = ["AM", "PM"]

class PathSelector:
    def __init__(self, prev = None):
        self.__paths = []
        self.current_path = prev
        self.__prev = prev

    def prev(self):
        return self.__prev

    def next(self):
        self.__prev = self.current_path
        if self.current_path == None:
            self.current_path = SmallSpike()
        else:
            if isinstance(self.current_path, UpDownUpDown):
                selection = random.random()
                if selection < .2:
                    self.current_path = UpDownUpDown()
                elif selection < .5:
                    self.current_path = BigSpike()
                elif selection < .65:
                    self.current_path = Decreasing()
                else:
                    self.current_path = SmallSpike()
            elif isinstance(self.current_path, BigSpike):
                selection = random.random()
                if selection < .5:
                    self.current_path = UpDownUpDown()
                elif selection < .55:
                    self.current_path = BigSpike()
                elif selection < .75:
                    self.current_path = Decreasing()
                else:
                    self.current_path = SmallSpike()
            elif isinstance(self.current_path, Decreasing):
                selection = random.random()
                if selection < .25:
                    self.current_path = UpDownUpDown()
                elif selection < .7:
                    self.current_path = BigSpike()
                elif selection < .75:
                    self.current_path = Decreasing()
                else:
                    self.current_path = SmallSpike()
            elif isinstance(self.current_path, SmallSpike):
                selection = random.random()
                if selection < .45:
                    self.current_path = UpDownUpDown()
                elif selection < .7:
                    self.current_path = BigSpike()
                elif selection < .85:
                    self.current_path = Decreasing()
                else:
                    self.current_path = SmallSpike()
        self.__paths.append(self.current_path.prices)
        return self.current_path

    def getAllPaths(self):
        return self.__paths

    def getAverageResults(self):
        avg = [0 for _ in range(len(DAYS) * 2)]
        for step_num in range(len(DAYS) * 2):
            for path in self.__paths:
                avg[step_num] += path[step_num]
        for i in range(len(avg)):
            avg[i] /= len(self.__paths)
        return avg

    def plot_paths(self, save_fig = False):
        for path in self.__paths:
            plt.plot(path)
        plt.ylabel("Price (Bells)")
        plt.xticks([n * 2 for n in range(7)], DAYS)
        plt.title(f"Turnip Price Paths over {len(self.__paths):,} Weeks")
        if save_fig:
            fileName = f"paths_{len(self.__paths)}.png"        
            output_dir = os.path.join(os.getcwd(), "output")
            if not os.path.exists(output_dir): os.mkdir(output_dir)
            path = os.path.join(output_dir, fileName)
            plt.savefig(path, bbox_inches="tight")
            print(f"Plot saved to {path}")
        else:
            plt.show()

    def plot_average(self, save_fig = False):
        plt.plot(self.getAverageResults())
        plt.ylabel("Price (Bells)")
        plt.xticks([n * 2 for n in range(7)], DAYS)
        plt.title(f"Average Turnip Price Paths over {len(self.__paths):,} Weeks")
        if save_fig:
            fileName = f"avg_paths_{len(self.__paths)}.png"        
            output_dir = os.path.join(os.getcwd(), "output")
            if not os.path.exists(output_dir): os.mkdir(output_dir)
            path = os.path.join(output_dir, fileName)
            plt.savefig(path, bbox_inches="tight")
            print(f"Plot saved to {path}")
        else:
            plt.show()

class TurnipPattern:
    def __init__(self, debug=False):
        self.base_price = random.randint(90, 110)
        self.prices = [self.base_price for _ in range(14)]
        self.runPattern(debug)
    
    def runPattern(self, debug = False):
        raise NotImplementedError
    
    def getName(self):
        raise NotImplementedError
    
    def __str__(self):
        result = []
        result.append(f"Base Price: {self.base_price}")
        for i in range(2, len(self.prices)):
            result.append(f"{DAYS[i // 2]} {TIMES[i % 2]}: {self.prices[i]}")
        return "\n".join(result)
    
    def plot(self, save_fig = False):
        plt.plot(self.prices)
        plt.xlabel("Day")
        plt.ylabel("Price")
        plt.xticks([n * 2 for n in range(7)], DAYS)
        plt.title(f"Turnip Price Path for {self.getName()}")
        if save_fig:
            fileName = f"{self.getName()}.png"        
            output_dir = os.path.join(os.getcwd(), "output")
            if not os.path.exists(output_dir): os.mkdir(output_dir)
            path = os.path.join(output_dir, fileName)
            plt.savefig(path, bbox_inches="tight")
            print(f"Plot saved to {path}")
        else:
            plt.show()
    
class UpDownUpDown(TurnipPattern):
    def getName(self):
        return "Up-Down-Up-Down"
    
    def runPattern(self, debug = False):
        duration_a = random.randint(0, 6) # 0-3 days
        duration_b = random.randint(2, 3) # 1-1.5 days
        duration_c = random.randint(1, 7 - duration_a) # 0.5-3.5 days
        duration_d = 5 - duration_b # 1-1.5 days
        duration_e = 7 - (duration_a + duration_c) # 0-3 days

        if debug:
            print(f"Phase A = {duration_a / 2:,} Days")
            print(f"Phase B = {duration_b / 2:,} Days")
            print(f"Phase C = {duration_c / 2:,} Days")
            print(f"Phase D = {duration_d / 2:,} Days")
            print(f"Phase E = {duration_e / 2:,} Days")

        phase_start = 2

        # Phase A: 0-3 Days, 90-140% of base price
        for i in range(duration_a):
            price = (random.randint(90, 140) * self.base_price) // 100
            self.prices[i + phase_start] = price
        phase_start += duration_a

        # Phase B: 1-1.5 Days, 60-80% of base price, then decreasing by 4-10% of base price
        price = (random.randint(60, 80) * self.base_price) // 100
        self.prices[phase_start] = price
        for i in range(1, duration_b):
            price -= (self.base_price * random.randint(4, 10)) // 100
            self.prices[i + phase_start] = price
        phase_start += duration_b

        # Phase C: 0.5-3.5 Days, 90-140% of base price
        for i in range(duration_c):
            price = (random.randint(90, 140) * self.base_price) // 100
            self.prices[i + phase_start] = price
        phase_start += duration_c

        # Phase D: 1-1.5 Days, 60-80% of base price, then decreasing by 4-10% of base price
        price = (random.randint(60, 80) * self.base_price) // 100
        self.prices[phase_start] = price
        for i in range(1, duration_d):
            price -= (self.base_price * random.randint(4, 10)) // 100
            self.prices[i + phase_start] = price
        phase_start += duration_d

        if duration_e > 0:
            # Phase E: 0-3 Days, 90-140% of base price
            for i in range(duration_e):
                price = (random.randint(90, 140) * self.base_price) // 100
                self.prices[i + phase_start] = price
            phase_start += duration_e

        if debug:
            print(f"phase start = {phase_start} (should be 14)")


class BigSpike(TurnipPattern):
    def getName(self):
        return "Big Spike"
    
    def runPattern(self, debug=False):
        duration_a = random.randint(1, 7) # 0.5-3.5 days
        duration_b = 2 # 1 day
        duration_c = 1 # 0.5 days
        duration_d = 2 # 1 day
        duration_e = 7 - duration_a # 0-3 days

        if debug:
            print(f"Phase A = {duration_a / 2:,} Days")
            print(f"Phase B = {duration_b / 2:,} Days")
            print(f"Phase C = {duration_c / 2:,} Days")
            print(f"Phase D = {duration_d / 2:,} Days")
            print(f"Phase E = {duration_e / 2:,} Days")

        phase_start = 2

        # Phase A: 0.5-3.5 Days, 85-90% of base price
        for i in range(duration_a):
            price = (random.randint(85, 90) * self.base_price) // 100
            self.prices[i + phase_start] = price
        phase_start += duration_a

        # Phase B: 1 Day, 90-140% of base price, then 140-200% of base price
        price = (random.randint(90, 140) * self.base_price) // 100
        self.prices[phase_start] = price
        for i in range(1, duration_b):
            price = (self.base_price * random.randint(140, 200)) // 100
            self.prices[i + phase_start] = price
        phase_start += duration_b

        # Phase C: 0.5 Days, 200-600% of base price
        for i in range(duration_c):
            price = (random.randint(200, 600) * self.base_price) // 100
            self.prices[i + phase_start] = price
        phase_start += duration_c

        # Phase D: 1 Day, 140-200% of base price, then 90-140% of base price
        price = (random.randint(140,  200) * self.base_price) // 100
        self.prices[phase_start] = price
        for i in range(1, duration_d):
            price = (self.base_price * random.randint(90, 140)) // 100
            self.prices[i + phase_start] = price
        phase_start += duration_d

        if duration_e > 0:
            # Phase E: 0-3 Days, 40-90% of base price
            for i in range(duration_e):
                price = (random.randint(40, 90) * self.base_price) // 100
                self.prices[i + phase_start] = price
            phase_start += duration_e

        if debug:
            print(f"phase start = {phase_start} (should be 14)")

class Decreasing(TurnipPattern):
    def getName(self):
        return "Decreasing"
    
    def runPattern(self, debug=False):
        duration_a = 12 # 6 days

        phase_start = 2
        # Phase A: 6 Days, 85-90% of base price, then decresing by 3-5% of base price
        price = (random.randint(85, 90) * self.base_price) // 100
        self.prices[phase_start] = price
        for i in range(1, duration_a):
            price -= (self.base_price * random.randint(3, 5)) // 100
            self.prices[i + phase_start] = price

class SmallSpike(TurnipPattern):
    def getName(self):
        return "Small Spike"

    def runPattern(self, debug=False):
        duration_a = random.randint(0, 7) # 0-3.5 days
        duration_b = 2 # 1 day
        duration_c = 1 # 0.5 days
        duration_d = 1 # 0.5 days
        duration_e = 1 # 0.5 days
        duration_f = 7 - duration_a # 0-3.5 days

        if debug:
            print(f"Phase A = {duration_a / 2:,} Days")
            print(f"Phase B = {duration_b / 2:,} Days")
            print(f"Phase C = {duration_c / 2:,} Days")
            print(f"Phase D = {duration_d / 2:,} Days")
            print(f"Phase E = {duration_e / 2:,} Days")
            print(f"Phase F = {duration_f / 2:,} Days")

        phase_start = 2

        # Phase A: 0-3.5 Days, 40-90% of base price, then decreasing by 3-5% of base price
        price = (random.randint(40, 90) * self.base_price) // 100
        self.prices[phase_start] = price
        for i in range(1, duration_a):
            price -= (random.randint(3, 5) * self.base_price) // 100
            self.prices[i + phase_start] = price
        phase_start += duration_a

        # Phase B: 1 Day, 90-140% of base price
        for i in range(1, duration_b):
            price = (self.base_price * random.randint(90, 140)) // 100
            self.prices[i + phase_start] = price
        phase_start += duration_b

        # Get price for phase D. It will be used for phases C and E.
        price_d = (random.randint(140, 200) * self.base_price) // 100

        # Phase C: 0.5 Days, between 140% of base price and the Phase D price
        for i in range(duration_c):
            price = random.randint((140 * self.base_price) // 100, price_d)
            self.prices[i + phase_start] = price
        phase_start += duration_c

        # Phase D: 0.5 Days, 140-200% of base price
        for i in range(duration_d):
            self.prices[i + phase_start] = price_d
        phase_start += duration_d

        # Phase E: 0.5 Days, between 140% of base price and the Phase D price
        for i in range(duration_e):
            price = random.randint((140 * self.base_price) // 100, price_d)
            self.prices[i + phase_start] = price
        phase_start += duration_e

        if duration_f > 0:
            # Phase F: 0-3.5 Days, 40-90% of base price, then decreasing by 3-5% of base price
            price = (random.randint(40, 90) * self.base_price) // 100
            self.prices[phase_start] = price
            for i in range(1, duration_f):
                price -= (random.randint(3, 5) * self.base_price) // 100
                self.prices[i + phase_start] = price
            phase_start += duration_f

        if debug:
            print(f"phase start = {phase_start} (should be 14)")
            print(self)
        

if __name__ == '__main__':
    ps = PathSelector()
    num_weeks = 1_000_000
    for week in range(num_weeks):
        print(f"\rRunning Week {week + 1:,}/{num_weeks:,}", end="")
        ps.next()
    print()
    #ps.plot_paths()
    ps.plot_average(save_fig=True)