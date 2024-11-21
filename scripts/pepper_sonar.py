import sys

class PepperSonar:
    def __init__(self, ALMemory):
        """
        Initializes the PepperSonar class with the ALMemory service.

        Args:
            ALMemory: The ALMemory service obtained from qi session.
        """
        self.memory_service = ALMemory
        self.memkey = {
            'SonarFront': 'Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value',
            'SonarBack': 'Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value'
        }

    def get_sonar_value(self, sonar_position):
        """
        Retrieve the current value of a specified sonar sensor.

        Args:
            sonar_position (str): Either 'SonarFront' or 'SonarBack'.

        Returns:
            float: The distance value of the sonar sensor.
        """
        try:
            value = self.memory_service.getData(self.memkey[sonar_position])
            return value
        except Exception as e:
            print(f"Error accessing {sonar_position} sonar: {e}")
            sys.stdout.flush()
            return float('inf')

    def scan_environment(self):
        """
        Check if a human is detected within 1.5 meters using the front sonar.

        Returns:
            bool: True if a human is detected within 1.5 meters, False otherwise.
        """
        # Read the front sonar value
        front_distance = self.get_sonar_value('SonarFront')

        # Check if human is within detection range (less than 1.5 meters)
        human_detected = front_distance < 1.5
        print("Human detected: {} at {:.2f} meters".format(
            'Yes' if human_detected else 'No', front_distance))
        sys.stdout.flush()
        return human_detected
