import grovepi
import zenoh
import sys
import signal
import json
import time


sensor = 6

blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.

z = zenoh.Zenoh(sys.argv[1], 'user'.encode(), 'password'.encode())
r_name = '/demo/temperature/orange'
print('Declaring publisher...')
pub = z.declare_publisher(r_name)


def catch_sig(sig, frame):
    z.close()
    exit(0)

signal.signal(signal.SIGINT, catch_sig)

while True:
    try:
        # This example uses the blue colored sensor.
        # The first parameter is the port, the second parameter is the type of sensor.
        grovepi.dht(sensor,white)
        [temp,humidity] = grovepi.dht(sensor,blue)
        msg = json.dumps({'temp':temp, 'hum':humidity})
        print('Sending {}'.format(msg))
        bs = bytearray()
        bs.append(len(msg))
        bs.extend(msg.encode())
        z.stream_data(pub, bytes(bs))
        time.sleep(1)

    except IOError:
        print ("Error")


# import time
# import grovepi

# #Sensor connected to A0 Port
# sensor = 0	# Pin 14 is A0 Port.
# grovepi.pinMode(sensor,"INPUT")
# while True:
#     try:
#         sensor_value = grovepi.analogRead(sensor)

#         print ("sensor_value = %d" %sensor_value)
#         time.sleep(.5)

#     except IOError:
#         print("Error")
