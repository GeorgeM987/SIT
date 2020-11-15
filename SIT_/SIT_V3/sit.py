import random
import time
#
from .table import wish_map
from .decorators import trinket_high


rpm_gauge = wish_map[0]
tps_gauge = [i[0] for i in wish_map]


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
    if len(outputs) > 10:
      outputs = outputs.clear()
      return outputs
    else:
      return x / len(outputs)


while True:

    frps_analog_in = random.randrange(0, 65536, 1)

    # #smothing the readings:
    # num_of_reads = 10
    # readings = [num_of_reads]
    # start_read_frps = 0
    # total_reads = 0
    # average = 0
    # total_reads = total_reads - readings[start_read_frps]
    # readings[start_read_frps] = frps_analog_in
    # total_reads = total_reads + readings[start_read_frps]
    # start_read_frps = start_read_frps + 1

    # if start_read_frps >= num_of_reads:
    #     start_read_frps = 0

    # average = total_reads / num_of_reads

    frps_maped_to_05 = float(map_val(frps_voltage_val(frps_analog_in), 0.0, 2.5, 0.0, 5.0))
    reads = []
    normalise(frps_maped_to_05, reads)
    
    if frps_maped_to_05 < 2.0:
        rpm_maped_to_05 = float(map_val(frps_maped_to_05, 0.0, 2.0, 0.0, 1.75))
    elif frps_maped_to_05 < 3.5:
        rpm_maped_to_05 = float(map_val(frps_maped_to_05, 2.0, 3.5, 2.25, 4.0))
    else:
        rpm_maped_to_05 = frps_maped_to_05

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