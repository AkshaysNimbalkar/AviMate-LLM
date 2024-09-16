import csv
import random
from datetime import datetime, timedelta

# Define parameters
start_time = datetime.strptime("06:00:00", "%H:%M:%S")
record_count = 5000
time_increment = timedelta(seconds=30)

# Flight and aircraft details
aircraft_types = ["Boeing 777", "Airbus A380", "Boeing 787", "Airbus A320", "Boeing 737 MAX"]
airlines = ["UAE", "ETD", "ABY", "FDB"]  # Emirates, Etihad, Air Arabia, FlyDubai
flight_numbers = [f"{airline}{str(num).zfill(3)}" for airline in airlines for num in range(100, 200)]
positions = [
    ("25.2532° N", "55.3657° E"),  # Dubai International Airport (OMDB)
    ("24.4560° N", "54.6374° E"),  # Abu Dhabi International Airport (OMAA)
    ("25.3286° N", "55.5171° E"),  # Sharjah International Airport (OMSJ)
    ("24.9180° N", "55.0728° E"),  # Al Maktoum International Airport (OMDW)
    ("26.0765° N", "56.2406° E"),  # Ras Al Khaimah International Airport (OMRK)
]
communication_types = ["ATC Instruction", "Pilot Acknowledgment", "Pilot Report", "Weather Update", "NOTAM Alert"]

communication_contents = {
    "ATC Instruction": [
        "Cleared for takeoff runway 30R.",
        "Climb and maintain {altitude} feet.",
        "Turn left heading {heading}, vectors for traffic.",
        "Descend and maintain {altitude} feet, expect ILS approach runway 09L.",
        "Contact departure on 125.5.",
        "Maintain present speed.",
        "Proceed direct to waypoint DESDI.",
        "Expect holding at waypoint PASOV.",
    ],
    "Pilot Acknowledgment": [
        "Cleared for takeoff runway 30R, {call_sign}.",
        "Climb and maintain {altitude} feet, {call_sign}.",
        "Left heading {heading}, {call_sign}.",
        "Descend to {altitude} feet, expect ILS 09L, {call_sign}.",
        "Switching to 125.5, {call_sign}.",
        "Maintaining present speed, {call_sign}.",
        "Proceeding direct to DESDI, {call_sign}.",
        "Holding at PASOV, {call_sign}.",
    ],
    "Pilot Report": [
        "Passing FL{flight_level}, climbing to FL380.",
        "Runway vacated, taxiing to gate.",
        "Established on localizer, runway in sight.",
        "Experiencing moderate turbulence at FL{flight_level}.",
        "Engine 2 showing abnormal vibrations.",
        "Requesting vectors for weather avoidance.",
        "Holding short of runway 12L, ready for departure.",
        "Cleared turbulence, resuming normal speed.",
    ],
    "Weather Update": [
        "Moderate turbulence reported at FL{flight_level}.",
        "Visibility reduced to 2 kilometers due to sandstorm at destination.",
        "Thunderstorms reported along your route near waypoint PASOV.",
        "Wind shear reported on final approach runway 30L.",
        "Icing conditions reported between FL180 and FL220 over the Hajar Mountains.",
    ],
    "NOTAM Alert": [
        "Runway 12R/30L closed from 2200Z to 0400Z.",
        "Navigation aid VOR DUB out of service.",
        "Temporary flight restriction active over area OM999.",
        "GPS interference reported near waypoint ORSAR.",
        "Airspace restriction due to military activity in Al Dhafra region.",
    ],
}

# Open CSV file for writing
with open('../data/pilot_assistant_data_uae.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write headers
    writer.writerow([
        "Time (UTC)", "Flight Number", "Call Sign", "Aircraft Type", "Communication Type",
        "Communication Content", "Altitude (ft)", "Speed (knots)", "Heading (degrees)",
        "Position (Latitude°, Longitude°)", "Weather Update", "NOTAMs",
        "Navigational Information", "Flight Manual Reference", "Summary"
    ])

    current_time = start_time
    for i in range(record_count):
        flight_number = random.choice(flight_numbers)
        call_sign = flight_number
        aircraft_type = random.choice(aircraft_types)
        comm_type = random.choice(communication_types)
        altitude = random.choice([0, 3000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 38000, 41000])
        speed = random.randint(0, 500)
        heading = random.randint(0, 360)
        position = random.choice(positions)
        weather_update = ""
        notams = ""
        navigational_info = "Waypoints: KUSBA, PASOV, DESDI"
        flight_manual_ref = ""
        summary = ""

        # Generate communication content
        comm_content_template = random.choice(communication_contents[comm_type])
        if "{altitude}" in comm_content_template:
            comm_content = comm_content_template.format(altitude=altitude, call_sign=call_sign)
        elif "{heading}" in comm_content_template:
            comm_content = comm_content_template.format(heading=heading, call_sign=call_sign)
        elif "{flight_level}" in comm_content_template:
            flight_level = altitude // 100
            comm_content = comm_content_template.format(flight_level=flight_level, call_sign=call_sign)
        else:
            comm_content = comm_content_template.format(call_sign=call_sign)

        # Additional logic based on communication type
        if comm_type == "Weather Update":
            weather_update = comm_content
            flight_manual_ref = "Refer to AOM Section 5"
            summary = "Weather update relevant to flight operations"
        elif comm_type == "NOTAM Alert":
            notams = comm_content
            summary = "NOTAM affecting flight operations"
        elif comm_type == "ATC Instruction":
            summary = "ATC provides instruction to aircraft"
        elif comm_type == "Pilot Acknowledgment":
            summary = "Pilot acknowledges instruction"
        elif comm_type == "Pilot Report":
            summary = "Pilot reports flight status"

        # Write row to CSV
        writer.writerow([
            current_time.strftime("%H:%M:%S"),
            flight_number,
            call_sign,
            aircraft_type,
            comm_type,
            comm_content,
            altitude,
            speed,
            heading,
            f"{position[0]}, {position[1]}",
            weather_update,
            notams,
            navigational_info,
            flight_manual_ref,
            summary
        ])

        # Increment time
        current_time += time_increment
