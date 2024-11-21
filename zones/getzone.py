#http://doc.aldebaran.com/2-5/naoqi/core/almemory-api.html
#http://doc.aldebaran.com/2-5/family/pepper_technical/pepper_dcm/actuator_sensor_names.html#ju-sonars

import qi
import argparse
import sys
import time
import threading

def setValueAlmemory(people_ids = [0]):
    return ["PeoplePerception/Person/" + str(person_id)+ "/EngagementZone" for person_id in people_ids]

engagementValueList = [
    "EngagementZones/PeopleInZone1",
    "EngagementZones/PeopleInZone2",
    "EngagementZones/PeopleInZone3" ]

import threading
import os

def rhMonitorThread (memory_service):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        engagementValues =  memory_service.getListData(engagementValueList)
        print ("[Zone1, Zone2, Zone3]", engagementValues)
        time.sleep(1)
    print("Exiting Thread")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["ZoneReader", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    #Starting services
    memory_service  = session.service("ALMemory")
      
    #create a thead that monitors directly the signal
    monitorThread = threading.Thread(target = rhMonitorThread, args = (memory_service,))
    monitorThread.start()

    #Program stays at this point until we stop it
    app.run()

    monitorThread.do_run = False
    
    print "Finished"


if __name__ == "__main__":
    main()
