# zones/getzone.py

import qi
import threading
import time

class EngagementZoneMonitor:
    def __init__(self, session):
        self.session = session
        self.memory_service = session.service("ALMemory")
        self.engagementValueList = [
            "EngagementZones/PeopleInZone1",
            "EngagementZones/PeopleInZone2",
            "EngagementZones/PeopleInZone3"
        ]
        self.monitor_thread = None
        self.running = False
        self.current_zones = [0, 0, 0]

    def start_monitoring(self):
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(target=self._monitor_thread)
            self.monitor_thread.start()

    def stop_monitoring(self):
        if self.running:
            self.running = False
            if self.monitor_thread is not None:
                self.monitor_thread.join()

    def _monitor_thread(self):
        while self.running:
            engagementValues = self.memory_service.getListData(self.engagementValueList)
            self.current_zones = engagementValues
            print("[Zone1, Zone2, Zone3]", engagementValues)
            time.sleep(1)
        print("Exiting Thread")

    def get_current_zones(self):
        return self.current_zones

