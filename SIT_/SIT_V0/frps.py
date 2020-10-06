import time
import random
#
# import board
# from analogio import AnalogIn
#
from decorators import *

table = [row for row in open('frps_table.txt', 'r')]
tps = [row[0:3] for row in table[1:11]]
rpm = list(table[0][4:-1].split(','))
# analog_in = AnalogIn(board.A1)

# def frps_voltage_val(pin):
#     return (pin.value * 3.3) / 65536
def frps_voltage_val(pin):
    return (pin * 3.3) / 65536

@adjust_voltage_val
def frps_vals(val_min: float=0.5, val_max: float=4.5) -> float:
    return val_min, val_max

def map_val(value, leftMin, leftMax, rightMin, rightMax):
    leftRange = leftMax - leftMin
    rightRange = rightMax - rightMin
    valuesScaled = float(value - leftMin) / float(leftRange)
    return '%g'%(rightMin + (valuesScaled * rightRange))

def rpm_to_tps_ratio(frps_rpm, frps_tps):

    @delta_t
    def in_range_25(start=0, stop=25, step=1, cof=5, wait=0.025):
        x_tps = frps_tps
        if x_tps in range(start, stop, step):
            x_rpm = frps_rpm
            if x_rpm <= 2000:
                mapped_rpm = int(map_val(x_tps, start, stop, 1000, 2000))
                x_rpm = round((x_rpm + mapped_rpm) / 2)
                for i in range(cof):
                    x_rpm -= 100
                    time.sleep(wait)
                return x_tps, x_rpm
    
    @delta_t
    def in_range_50(start=25, stop=50, step=1, cof=4, wait=0.025):
        x_tps = frps_tps
        if x_tps in range(start, stop, step):
            x_rpm = frps_rpm
            if x_rpm <= 3000:
                mapped_rpm = int(map_val(x_tps, start, stop, 2000, 3000))
                x_rpm = round((x_rpm + mapped_rpm) / 2)
                for i in range(cof):
                    x_rpm -= 100
                    time.sleep(wait)
                return x_tps, x_rpm
    
    @delta_t
    def in_range_75(start=50, stop=75, step=1, cof=3, wait=0.025):
        x_tps = frps_tps
        if x_tps in range(start, stop, step):
            x_rpm = frps_rpm
            if x_rpm <= 4000:
                mapped_rpm = int(map_val(x_tps, start, stop, 3000, 4000))
                x_rpm = round((x_rpm + mapped_rpm) / 2)
                for i in range(cof):
                    x_rpm -= 100
                    time.sleep(wait)
                return x_tps, x_rpm
    
    @delta_t
    def in_range_100(start=75, stop=100, step=1, cof=2, wait=0.025):
        x_tps = frps_tps
        if x_tps in range(start, stop, step):
            x_rpm = frps_rpm
            if x_rpm <= 4500:
                mapped_rpm = int(map_val(x_tps, start, stop, 4000, 4500))
                x_rpm = round((x_rpm + mapped_rpm) / 2)
                for i in range(cof):
                    x_rpm -= 100
                    time.sleep(wait)
                return x_tps, x_rpm
    try:
        if frps_tps <= 25 and in_range_25()[-1][0:] != None:
            return list(in_range_25()[-1][0:])
        elif frps_tps > 25 and frps_tps <= 50 and in_range_50()[-1][0:] != None:
            return list(in_range_50()[-1][0:])
        elif frps_tps > 50 and frps_tps <= 75 and in_range_75()[-1][0:] != None:
            return list(in_range_75()[-1][0:])
        elif frps_tps > 75 and in_range_100()[-1][0:] != None:
            return list(in_range_100()[-1][0:])
        else:
            return [frps_tps, frps_rpm]

    except TypeError as e:
        if 'NoneType' in str(e):
            return [frps_tps, frps_rpm]
        else:
            raise

    finally:
        pass

while True:
    
    analog_in = random.randrange(18350, 65536, 1)
    frps_maped_to_05 = float(map_val(frps_voltage_val(analog_in), 0.0, 3.3, frps_vals()[0], frps_vals()[-1]))
    frps_to_tps_ratio = round(float(map_val(frps_maped_to_05, 0.5, 4.5, float(tps[0]), float(tps[-1]))))
    frps_to_rpm_ratio = round(float(map_val(frps_maped_to_05, 0.5, 4.5, float(rpm[0]), float(rpm[-1]))))

    tps_and_rpm = rpm_to_tps_ratio(frps_to_rpm_ratio, frps_to_tps_ratio)

    for i in tps_and_rpm[:-1]:
        tps_match = min(tps, key=lambda x: abs(int(x)-i))

    for i in tps_and_rpm[-1:]:
        rpm_match = min(rpm, key=lambda x: abs(int(x)-i))

    try:
        for i in table:
            for i2 in range(int(i[0:][:3]), int(tps_match), int(tps_match)):
                k = [x for x in enumerate(i[:i.index(rpm_match) + 4].split(','))]
                for x, y in k[-1:]:
                    for t in table[:int(tps_match[:-1]) + 1]:
                        mapped_table = t[:i.index(y) + 9].strip(',')
                        print(mapped_table)
            # print(rpm_match)
            # print(tps_match)
            # print(mapped_table[-3:])

    except ValueError as e:
        if 'substring not found' in str(e):
            time.sleep(1)
            print('#' * 50)
            continue