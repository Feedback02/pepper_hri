# Sonar simulation using memory keys
#
# Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value
# Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value

import qi
import argparse
import sys
import time
import threading
import os


memkey = {
    'zone1': 'EngagementZones/PeopleInZone1',
    'zone2': 'EngagementZones/PeopleInZone2',
    'zone3': 'EngagementZones/PeopleInZone3'}



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--zone", type=str, default="Zone2",
                        help="zone: Zone1, Zone2, Zone3")
    parser.add_argument("--id", nargs='*',type=int,
                        help="People ids in the zone")
    parser.add_argument("--duration", type=float, default=3.0,
                        help="Duration of the event")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["ZoneSim", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    #Starting services
    memory_service  = session.service("ALMemory")

    val = None
    try:
        val = args.id
    except:
        print("ERROR")
        return

    try:
        mkey = memkey[args.zone]
        print("Zones" + args.zone + " = ",val)
        print(val)
        memory_service.insertData(mkey,val)
        time.sleep(args.duration)
        memory_service.insertData(mkey,[])
    except:
        print("ERROR: Zone %s unknown" %args.zone)

if __name__ == "__main__":
    main()
