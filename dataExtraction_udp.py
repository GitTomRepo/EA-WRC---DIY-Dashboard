import struct
import time
from datetime import timedelta
import socket
import matplotlib.pyplot as plt
import serial

UDP_IP = "127.0.0.1"
UDP_PORT = 20777

PRINT_INFO = False

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(5)

arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1) 

dataCapture_duration = time.time() + 60*3

time_values = []
throttle = []
brake = []
speed = []

while True :
    try :
        byteChaine = sock.recv(256)

        arduino.write(byteChaine) 

        vehicle_gear_index = byteChaine[0]
        vehicle_gear_maximum = byteChaine[1]
        vehicle_speed = struct.unpack('f', byteChaine[2:6])[0]*3.6
        vehicle_engine_rpm_max = struct.unpack('f', byteChaine[6:10])[0]
        vehicle_engine_rpm_current = struct.unpack('f', byteChaine[10:14])[0]
        vehicle_throttle = struct.unpack('f', byteChaine[14:18])[0]*100
        vehicle_brake = struct.unpack('f', byteChaine[18:22])[0]*100
        vehicle_clutch = struct.unpack('f', byteChaine[22:26])[0]*100
        vehicle_steering = struct.unpack('f', byteChaine[26:30])[0]*100
        vehicle_handbrake = struct.unpack('f', byteChaine[30:34])[0]*100
        stage_current_time = timedelta(seconds=struct.unpack('f', byteChaine[34:38])[0])
        stage_current_distance = struct.unpack('d', byteChaine[38:46])[0]/1000
        stage_length = struct.unpack('d', byteChaine[46:54])[0]/1000

        if PRINT_INFO :
            print(f"Gear : {vehicle_gear_index}")
            print(f"Max Gear : {vehicle_gear_maximum}")
            print(f"Speed : {vehicle_speed} km/h")
            print(f"Max RPM : {vehicle_engine_rpm_max}")
            print(f"RPM : {vehicle_engine_rpm_current}")
            print(f"Throttle : {vehicle_throttle}%")
            print(f"Brake : {vehicle_brake}%")
            print(f"Clutch : {vehicle_clutch}%")
            print(f"Steering : {vehicle_steering}%")
            print(f"Handbrake : {vehicle_handbrake}%")
            print(f"Time : {stage_current_time}")
            print(f"Current distance : {stage_current_distance} km")
            print(f"Stage length : {stage_length} km")

        time_values.append(stage_current_time.total_seconds())
        throttle.append(vehicle_throttle)
        brake.append(vehicle_brake)
        speed.append(vehicle_speed)

        if time.time() > dataCapture_duration :
            break
    except :
        print("ERRO - Time OUT")
        break

if (len(time_values) > 0) :
    plt.figure("UDP - EA WRC")

    plt.subplot(2, 1, 1)
    plt.title("Telemetry : Throttle / Brake (in %)")
    plt.plot(time_values, throttle, 'green', linewidth=0.5)
    plt.plot(time_values, brake, 'red', linewidth=0.5)
    plt.legend(['Throttle', 'Brake'])

    plt.subplot(2, 1, 2)
    plt.title("Telemetry : Speed (in km/h)")
    plt.plot(time_values, speed, 'blue', linewidth=1)
    plt.legend(['Speed'])

    plt.subplots_adjust(left=0.1,
                        bottom=0.1, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.4, 
                        hspace=0.4)
    plt.show()
else :
    print("ERROR - No values")