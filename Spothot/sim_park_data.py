
import json, random, time
from datetime import datetime
import subprocess
import boto3



# Sample street names for realismr
STREETS = [
    "N Central Ave", "E Washington St", "W Jefferson St",
    "E Van Buren St", "W Adams St", "E Monroe St",
    "N 1st Ave", "N 3rd St", "E Roosevelt St"
]

# Zip codes for Phoenix Downtown area
ZIP_CODES = [85003, 85004, 85007]

# Sample zones for pricing/parking policy
ZONES = ["Zone A", "Zone B", "Zone C"]

# Sample coordinates near Phoenix Downtown with additional metadata
PARKING_SPOTS = [
    {
        "id": f"P{i+1}",
        "latitude": 33.4484 + random.uniform(-0.005, 0.005),
        "longitude": -112.0740 + random.uniform(-0.005, 0.005),
        "street": random.choice(STREETS),
        "zipcode": random.choice(ZIP_CODES),
        "city": "Phoenix",
        "zone": random.choice(ZONES)
    }
    for i in range(50)
]

def generate_parking_data():
    data = []
    for spot in PARKING_SPOTS:
        status = random.choice(["available", "occupied"])
        record = {
            "id": spot["id"],
            "location": {
                "latitude": spot["latitude"],
                "longitude": spot["longitude"],
                "street": spot["street"],
                "zipcode": spot["zipcode"],
                "city": spot["city"]
            },
            "zone": spot["zone"],
            "status": status,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        data.append(record)
    return data


# Function to generate & upload data
def generate_and_upload():
    with open("simulated_parking_data.json", "w") as f:
        json.dump(generate_parking_data(), f, indent=2)

    subprocess.run([
        "aws", "s3", "cp", "simulated_parking_data.json",
        "s3://phoenix-parking-data-bucket/"
    ], check=True)

    print(f"Uploaded updated parking data at {datetime.utcnow().isoformat()}Z")

# Loop: run once every 24 hours
while True:
    generate_and_upload()
    time.sleep(86400)