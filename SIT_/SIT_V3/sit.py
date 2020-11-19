import random
import time
#
from .table import wish_map


rpm_gauge = wish_map[0]
tps_gauge = [i[0] for i in wish_map]
reads = []


def frps_voltage_val(pin):
    return pin * 2.5 / 65536


def map_val(value, leftMin, leftMax, rightMin, rightMax):
    leftRange = leftMax - leftMin
    rightRange = rightMax - rightMin
    valuesScaled = float(value - leftMin) / float(leftRange)
    return '%g'%(rightMin + (valuesScaled * rightRange))


def normalise(inputs, outputs):
    x = 0
    outputs.append(inputs)
    for o in outputs:
        x += o
    if len(outputs) > 3:
        outputs.clear()
        return inputs
    else:
        return x / len(outputs)

while True:

    frps_analog_in = random.randrange(0, 65536, 1)
    frps_maped_to_05 = float(map_val(frps_voltage_val(frps_analog_in), 0.0, 2.5, 0.0, 5.0))
    frps_normalised = normalise(frps_maped_to_05, reads)

    if frps_normalised < 2.0:
        rpm_normalised = float(map_val(frps_normalised, 0.0, 2.0, 0.0, 1.75))
    elif frps_normalised < 3.5:
        rpm_normalised = float(map_val(frps_normalised, 2.0, 3.5, 2.25, 4.0))
    else:
        rpm_normalised = frps_normalised

    tps = round(float(map_val(frps_normalised, 0.0, 5.0, tps_gauge[0], tps_gauge[-1])))
    rpm = round(float(map_val(rpm_normalised, 0.0, 5.0, rpm_gauge[0], rpm_gauge[-1])))
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