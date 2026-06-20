import json
import threading
import time

from structures.dataclasses import SensorReading


class IndoorAirData(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.temperature_c = 0
        self.humidity = 0
        self.co2_ppm = 0
 
    def run(self):
        path = "/opt/bme680-raspberry-pi-driver/src/examples/m5_stack/latest.json"
        while True:
            try:
                with open(path) as f:
                    data = json.load(f)
                self.temperature_c = data["temperature"]
                self.humidity = round(data["humidity"])
                self.co2_ppm = round(data["co2_equivalent"])
            except Exception:
                pass
            time.sleep(2)
 
    def get_data(self):
        return SensorReading(self.temperature_c, self.humidity, self.co2_ppm)
