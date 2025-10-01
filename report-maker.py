# --- DEL A ---
# --- Task 1 : Read JSON file , list company name, and when last updated. ---

# --- Redirect all print output to report.txt ---
import sys

report_file = open("report.txt", "w", encoding="utf-8")  # Öppnar filen och skriver över gamla innehållet

class Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, text):
        for f in self.files:
            f.write(text)
    def flush(self):
        for f in self.files:
            f.flush()

# Redirect stdout till både terminalen och filen
sys.stdout = Tee(sys.stdout, report_file)

# Import the json library so that we can handle json

import json

# Opens and reads the JSON file.
with open("network_devices.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# fetches the company names and the last update.
company_name = data["company"]
last_updated = data["last_updated"]

# Writes to the terminal
print(f"Företag: {company_name}")
print(f"Senast uppdaterad: {last_updated}")

# --- Task 2 : Lists the devices with problems. ---

for location in data["locations"]:
    for device in location["devices"]:
        if device["status"] in ["offline", "warning"]:
            print(f"- {device['hostname']} ({device['type']}) "
                  f"på {location['site']} i {location['city']} → STATUS: {device['status']}")

# --- Task 3 : Count total number of devices per type. ---

device_count = {}

for location in data["locations"]:
    for device in location["devices"]:
        dtype = device["type"]
        device_count[dtype] = device_count.get(dtype, 0) + 1

print("\nTotal number of devices per type:")
for dtype, count in device_count.items():
    print(f"- {dtype}: {count}")

# --- Task 4 : List all devices with less than 30 days uptime. ---

print("\nEnheter med mindre än 30 dagars uptime:")

for location in data["locations"]:
    for device in location["devices"]:
        if device.get("uptime_days", 0) < 30:
            print(f"- {device['hostname']} ({device['type']}) "
                  f"på {location['site']} i {location['city']} → Uptime: {device['uptime_days']} dagar")

# --- DEL B ---
# --- Task 5 : Total port usage for all switches ---

total_ports = 0
used_ports = 0

for location in data["locations"]:
    for device in location["devices"]:
        if device["type"] == "switch":
            ports_info = device.get("ports", {})
            total_ports += ports_info.get("total", 0)
            used_ports += ports_info.get("used", 0)

# Beräkna procent användning
percent_used = (used_ports / total_ports * 100) if total_ports else 0

print("\nTotal portanvändning för alla switchar:")
print(f"- Använda portar: {used_ports}")
print(f"- Totala portar: {total_ports}")
print(f"- Procentuellt använda: {percent_used:.2f}%")

# --- Task 6 : List all unique VLANs in the network ---

unique_vlans = set()

for location in data["locations"]:
    for device in location["devices"]:
        vlans = device.get("vlans", [])
        for vlan in vlans:
            unique_vlans.add(vlan)

# Sortera VLANs för snygg utskrift
sorted_vlans = sorted(unique_vlans)

print("\nAlla unika VLAN som används i nätverket:")
print(sorted_vlans)

# --- Task 7 : Overview per location (total devices, online/offline counts) ---

print("\nÖversikt per lokation:")

for location in data["locations"]:
    total_devices = len(location["devices"])
    online_count = sum(1 for d in location["devices"] if d["status"] == "online")
    offline_count = sum(1 for d in location["devices"] if d["status"] == "offline")
    warning_count = sum(1 for d in location["devices"] if d["status"] == "warning")
    
    print(f"- {location['site']} i {location['city']}:")
    print(f"  Totalt antal enheter: {total_devices}")
    print(f"  Online: {online_count}")
    print(f"  Offline: {offline_count}")
    print(f"  Warning: {warning_count}")

