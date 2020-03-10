import serial
import time

#ard_vars = [<pulse>, <gsr>]
def ardThread(port, speed, ard_vars, lock):
    global pulse

    ser = serial.Serial(port, 115200)
    time.sleep(3)

    pulses = []
    isCalibrating = False

    KEYS = "P"
    pulse = 0

    print('Reader started')
    t0 = time.time()
    while True:
        recv = ser.read().decode('utf-8');
        if recv == "P":
            num = ''
            while True:
                recv = ser.read().decode('utf-8')

                if recv == 'p':
                    break

                num += recv

            pulse = int(num.split('.')[0])

        if (time.time() - t0 > 10):
            with lock:
                ard_vars[0] = pulse
                pulses.append(pulse)


            t0 = time.time()

        with lock:
            if ard_vars[3] and not isCalibrating:
                print('CALIBRATING\n'*5)
                isCalibrating = True
                pulses = []

            if isCalibrating and not ard_vars[3]:
                isCalibrating = False
                ard_vars[1] = sum(pulses)/len(pulses)


