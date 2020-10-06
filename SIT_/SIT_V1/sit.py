import random
import time
#
from .table import wish_map
from .decorators import trinket_high


rpm_gauge = wish_map[0]
tps_gauge = [i[0] for i in wish_map]


@trinket_high
def frps_voltage_val(pin):
    return pin * 2.5

@trinket_high
def rpm_voltage_val(pin):
    return pin * 3.3

def map_val(value, leftMin, leftMax, rightMin, rightMax):
    leftRange = leftMax - leftMin
    rightRange = rightMax - rightMin
    valuesScaled = float(value - leftMin) / float(leftRange)
    return '%g'%(rightMin + (valuesScaled * rightRange))


while True:

    frps_analog_in = random.randrange(0, 65536, 1)
    rpm_analog_in = random.randrange(0, 65536, 1)
    frps_maped_to_05 = float(map_val(frps_voltage_val(frps_analog_in), 0.0, 2.5, 0.0, 5.0))
    rpm_maped_to_05 = float(map_val(rpm_voltage_val(rpm_analog_in), 0.0, 3.3, 0.0, 5.0))
    tps = round(float(map_val(frps_maped_to_05, 0.0, 5.0, tps_gauge[0], tps_gauge[-1])))
    rpm = round(float(map_val(rpm_maped_to_05, 0.0, 5.0, rpm_gauge[0], rpm_gauge[-1])))
    tps_match = min(tps_gauge, key=lambda x: abs(int(x) - tps))
    rpm_match = min(rpm_gauge, key=lambda x: abs(int(x) - rpm))

    try:
        for i in wish_map:
            for i2 in wish_map:
                if i2[0] <= tps_match:
                    print(i2[:i.index(rpm_match)])
                    
    except ValueError as e:
        if 'not found' in str(e) or 'not in list' in str(e):
            time.sleep(1)
            print('#' * 50)
            continue

    time.sleep(1)