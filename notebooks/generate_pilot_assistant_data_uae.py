# Let's generate sample datasets for all the required data sources: ATC communications, weather, historical incidents, flight manuals, fuel management, and NOTAMs.
import csv
import random
from datetime import datetime, timedelta

# Define common parameters
start_time = datetime.strptime("00:00:00", "%H:%M:%S")
end_time = datetime.strptime("23:59:59", "%H:%M:%S")
time_increment = timedelta(seconds=30)  # Frequent communication intervals

# Create separate datasets for each source
datasets = {
    "atc_communications": [],
    "weather": [],
    "historical_incidents": [],
    "flight_manuals": [],
    "fuel_management": [],
    "notams": [],
    "flight_performance" : [],
    "aircraft_systems_status": [],
    "real_time_air_traffic": [],
    "waypoint_and_route_info": [],
    "airport_operations_status": [],
    "emergency_procedures": [],
    "cargo_and_weight_management": [],
    "crew_and_passenger_status": [],
    "weather_predictions": [],
    "flight_plan_monitoring": [],
    "satellite_communication_status": []
}

# Flight-specific details
flight_number = "EK201"
call_sign = "UAE201"
aircraft_type = "Boeing 777"

# Positions for the flight path
positions = [
    ("25.2532° N", "55.3657° E"),  # Departure: Dubai International Airport (OMDB)
    ("26.0765° N", "56.2406° E"),  # Waypoint 1
    ("28.7041° N", "77.1025° E"),  # Waypoint 2
    ("34.0837° N", "74.7973° E"),  # Waypoint 3
    ("40.6413° N", "-73.7781° W")  # Arrival: John F. Kennedy International Airport (JFK)
]

# Random data generators for various datasets
def generate_atc_communication():
    comm_types = ["ATC Instruction", "Pilot Acknowledgment", "Pilot Report"]
    comm_type = random.choice(comm_types)
    altitudes = [5000, 10000, 15000, 20000, 25000, 30000, 35000]
    messages = {
        "ATC Instruction": [
            "Cleared for takeoff runway 09L.",
            "Climb and maintain {altitude} feet.",
            "Turn left heading {heading}, vectors for traffic.",
            "Descend and maintain {altitude} feet, expect ILS approach runway 27.",
            "Contact departure on 124.7.",
            "Maintain present speed.",
            "Proceed direct to waypoint ALPHA.",
            "Expect holding at waypoint BRAVO.",
            "Reduce speed to 250 knots.",
            "Climb to FL{flight_level} and maintain.",
            "Hold short of runway 12R.",
            "Taxi to gate via taxiway Bravo.",
            "Descend to {altitude} feet and prepare for approach.",
            "Cross runway 09L and continue taxi to terminal.",
            "Switch to ground control on 121.9.",
            "Expect vectors for ILS approach to runway 13R.",
            "Contact center on 126.1 for further instructions.",
            "Request speed reduction due to traffic ahead.",
            "Proceed to final approach and maintain {altitude} feet."
        ],
        "Pilot Acknowledgment": [
            "Climb and maintain {altitude} feet, {call_sign}.",
            "Turning left heading {heading}, {call_sign}.",
            "Descending to {altitude} feet, expect ILS runway 27, {call_sign}.",
            "Switching to 124.7, {call_sign}.",
            "Maintaining present speed, {call_sign}.",
            "Proceeding direct to ALPHA, {call_sign}.",
            "Holding at BRAVO, {call_sign}.",
            "Reducing speed to 250 knots, {call_sign}.",
            "Climbing to FL{flight_level}, {call_sign}.",
            "Holding short of runway 12R, {call_sign}.",
            "Taxiing to gate via taxiway Bravo, {call_sign}.",
            "Descending to {altitude} feet, {call_sign}.",
            "Crossing runway 09L, continuing to terminal, {call_sign}.",
            "Switching to ground control on 121.9, {call_sign}.",
            "Proceeding to final approach, maintaining {altitude} feet, {call_sign}."
        ],
        "Pilot Report": [
            "Passing FL{flight_level}, climbing to FL350.",
            "Runway vacated, taxiing to gate.",
            "Established on localizer, runway in sight.",
            "Experiencing moderate turbulence at FL{flight_level}.",
            "Engine 2 showing abnormal vibrations.",
            "Requesting vectors for weather avoidance.",
            "Holding short of runway 22R, ready for departure.",
            "Cleared turbulence, resuming normal speed."
        ]
    }
    
    content = random.choice(messages[comm_type])
    altitude = random.choice(altitudes)
    heading = random.randint(0, 360)
    flight_level = altitude // 100
    message_content = content.format(altitude=altitude, heading=heading, flight_level=flight_level, call_sign=call_sign)

    return [comm_type, message_content, altitude, random.randint(400, 500), heading, random.choice(positions)]

def generate_weather():
    weather_conditions = ["Clear", "Moderate Turbulence", "Thunderstorms", "Fog", "Icing Conditions"]
    wind_speeds = ["10 knots", "15 knots", "20 knots"]
    return [random.choice(positions), random.choice(weather_conditions), random.choice(wind_speeds), f"{random.randint(20, 35)}°C"]

# Adding more historical incidents to the generation process

def generate_historical_incidents():
    incidents = [
        "Engine Failure",
        "Bird Strike",
        "Medical Emergency",
        "Severe Turbulence",
        "Hydraulic System Failure",
        "Landing Gear Malfunction",
        "Fuel Leak Detected",
        "Mid-Air Collision Avoidance Maneuver",
        "Cabin Pressure Loss",
        "Navigation System Failure",
        "Passenger Disturbance",
        "Smoke in Cabin",
        "Avionics Failure",
        "Runway Incursion",
        "Unstable Approach Detected",
        "Wind Shear on Approach",
        "Fire in Engine Compartment",
        "Emergency Descent",
        "Structural Damage Due to Turbulence",
        "Incorrect Altimeter Settings"
    ]
    
    actions = {
        "Engine Failure": "Declared emergency, initiated emergency landing.",
        "Bird Strike": "Requested immediate return to origin, engine inspection required.",
        "Medical Emergency": "Requested priority landing, medical personnel on standby.",
        "Severe Turbulence": "Requested altitude change, secured cabin.",
        "Hydraulic System Failure": "Switched to backup hydraulics, diverted to nearest airport.",
        "Landing Gear Malfunction": "Conducted low approach for visual inspection, prepared for emergency landing.",
        "Fuel Leak Detected": "Declared emergency, diverted to alternate airport, initiated fuel dumping.",
        "Mid-Air Collision Avoidance Maneuver": "Performed evasive maneuver, resumed normal operations after clearance.",
        "Cabin Pressure Loss": "Initiated emergency descent to 10,000 feet, oxygen masks deployed.",
        "Navigation System Failure": "Switched to backup navigation systems, continued flight under manual control.",
        "Passenger Disturbance": "Crew handled disturbance, notified ATC, police on standby at destination.",
        "Smoke in Cabin": "Declared emergency, diverted to nearest airport, passengers evacuated.",
        "Avionics Failure": "Continued flight using backup systems, prepared for manual landing.",
        "Runway Incursion": "Aborted takeoff, instructed to hold position, waited for clearance.",
        "Unstable Approach Detected": "Conducted go-around, prepared for second approach.",
        "Wind Shear on Approach": "Aborted landing, climbed to safe altitude, awaited further instructions.",
        "Fire in Engine Compartment": "Declared emergency, initiated fire suppression, diverted to nearest airport.",
        "Emergency Descent": "Rapid descent initiated due to medical emergency, cleared by ATC.",
        "Structural Damage Due to Turbulence": "Requested emergency landing, conducted visual inspection after landing.",
        "Incorrect Altimeter Settings": "Adjusted altimeter settings, re-calculated descent approach."
    }
    
    incident = random.choice(incidents)
    action_taken = actions[incident]
    delay = random.randint(0, 90)  # Random delay in minutes due to incident
    return [incident, action_taken, delay, f"Incident: {incident}, Action: {action_taken}"]

# Re-run the process to create the datasets with more diverse historical incidents

# Expanding the Flight Manual dataset generation with more detailed instructions

def generate_flight_manual():
    sections = [
        "AOM Section 1",
        "AOM Section 2",
        "AOM Section 3",
        "AOM Section 4",
        "AOM Section 5",
        "AOM Section 6",
        "AOM Section 7",
        "AOM Section 8",
        "AOM Section 9",
        "AOM Section 10",
        "QRH Section 1",
        "QRH Section 2",
        "QRH Section 3",
        "FCOM Section 1",
        "FCOM Section 2",
        "FCOM Section 3",
        "FCOM Section 4",
        "FCOM Section 5"
    ]

    scenarios = [
        "Engine Failure",
        "Turbulence",
        "Icing Conditions",
        "Hydraulic Failure",
        "Cabin Pressure Loss",
        "Fire in Engine",
        "Navigation System Failure",
        "Electrical Failure",
        "Landing Gear Malfunction",
        "Smoke in Cabin",
        "Engine Overheating",
        "Bird Strike",
        "Fuel Leak",
        "Brake Failure",
        "Instrument Failure",
        "Airspeed Indicator Malfunction",
        "Stall Warning",
        "Decompression",
        "Runway Overrun",
        "Emergency Evacuation"
    ]

    instructions = {
        "Engine Failure": [
            "Throttle idle, apply maximum climb, contact ATC for emergency landing clearance.",
            "Maintain heading, attempt engine restart procedures, prepare for single-engine operation."
        ],
        "Turbulence": [
            "Reduce speed to turbulence penetration speed, secure cabin and prepare for altitude change.",
            "Notify passengers, adjust flight path to avoid turbulent area, monitor weather updates."
        ],
        "Icing Conditions": [
            "Activate anti-ice systems, monitor fuel temperature, consider altitude change.",
            "Report icing conditions to ATC, request vector to exit icing area, perform de-icing procedures."
        ],
        "Hydraulic Failure": [
            "Switch to backup hydraulic system, contact ATC for nearest airport diversion.",
            "Implement manual flight controls, reduce speed, prepare for manual landing."
        ],
        "Cabin Pressure Loss": [
            "Descend to 10,000 feet, ensure oxygen masks are deployed, contact ATC for emergency descent.",
            "Activate emergency pressurization system, monitor cabin altitude, brief cabin crew."
        ],
        "Fire in Engine": [
            "Shut down affected engine, activate fire suppression system, prepare for emergency landing.",
            "Declare Mayday, divert to nearest suitable airport, advise cabin crew and passengers."
        ],
        "Navigation System Failure": [
            "Switch to backup navigation system, continue flight under manual control, prepare for manual landing.",
            "Use radio navigation aids, coordinate with ATC for heading and altitude information."
        ],
        "Electrical Failure": [
            "Switch to backup power system, reduce non-essential loads, contact ATC for diversion.",
            "Use emergency power supply, monitor critical systems, prepare for possible communication loss."
        ],
        "Landing Gear Malfunction": [
            "Attempt manual gear extension, prepare for low approach for visual inspection, prepare for emergency landing.",
            "Inform ATC of gear issue, perform alternate gear extension procedures, consider belly landing if necessary."
        ],
        "Smoke in Cabin": [
            "Declare emergency, initiate cabin smoke removal procedures, divert to nearest airport.",
            "Advise cabin crew to locate source of smoke, prepare passengers for possible evacuation."
        ],
        "Engine Overheating": [
            "Reduce thrust on affected engine, monitor temperature gauges, prepare for potential engine shutdown.",
            "Adjust fuel mixture, increase airspeed to cool engine, declare emergency if temperature rises."
        ],
        "Bird Strike": [
            "Assess aircraft for damage, monitor engine performance, prepare for possible diversion.",
            "Inform ATC of bird strike, request immediate return to airport if necessary."
        ],
        "Fuel Leak": [
            "Isolate affected fuel tank, crossfeed from other tanks, calculate remaining fuel for diversion.",
            "Declare emergency, avoid areas where fuel leak could cause hazard, prepare for immediate landing."
        ],
        "Brake Failure": [
            "Plan for longer landing rollout, use reverse thrust and spoilers effectively, inform ATC.",
            "Consider diverting to airport with longer runway, prepare for possible runway excursion."
        ],
        "Instrument Failure": [
            "Switch to standby instruments, maintain visual flight rules if possible, inform ATC.",
            "Use co-pilot's instruments if available, prepare for approach using backup systems."
        ],
        "Airspeed Indicator Malfunction": [
            "Cross-check with other airspeed indicators, use GPS groundspeed as reference, avoid abrupt maneuvers.",
            "Activate pitot heat, suspect pitot-static system blockage, prepare for unreliable airspeed procedure."
        ],
        "Stall Warning": [
            "Lower nose to reduce angle of attack, increase throttle to regain airspeed, avoid abrupt inputs.",
            "Verify stall warning accuracy, monitor airspeed and altitude, prepare for possible emergency descent."
        ],
        "Decompression": [
            "Don oxygen masks, initiate emergency descent, inform ATC and passengers.",
            "Check cabin pressure indicators, prepare for possible hypoxia symptoms, divert to suitable airport."
        ],
        "Runway Overrun": [
            "Apply maximum braking, deploy spoilers and reverse thrust, prepare for possible evacuation.",
            "Inform ATC, avoid obstacles beyond runway, assess aircraft damage after stop."
        ],
        "Emergency Evacuation": [
            "Stop aircraft, initiate evacuation procedures, coordinate with cabin crew.",
            "Ensure engines and systems are shut down, assist passengers as needed, inform emergency services."
        ]
    }

    generated_records = set()

    while len(generated_records) < 300:
        section = random.choice(sections)
        scenario = random.choice(scenarios)
        instruction = random.choice(instructions[scenario])
        record = (section, scenario, instruction)
        generated_records.add(record)

    # Convert set of tuples to list of lists
    return [list(record) for record in generated_records]


# Re-run the process to create the dataset with more detailed flight manual entries

def generate_fuel_data():
    return [random.randint(5000, 30000), random.randint(5000, 20000), random.randint(2000, 5000), "Normal fuel burn."]

# Adding more NOTAM messages with timestamps

def generate_notam():
    notam_messages = [
        "Runway 09L closed for maintenance from 2200Z to 0600Z.",
        "Navigation aid VOR XYZ out of service until further notice.",
        "Temporary flight restriction active over area OM999 due to military activity.",
        "GPS interference reported near waypoint DELTA from 0300Z to 0600Z.",
        "Runway 13L under inspection, expect delays.",
        "ILS system out of service for runway 27 until further notice.",
        "Taxiway Bravo closed for resurfacing from 1200Z to 1800Z.",
        "Expect delays due to heavy air traffic at KJFK between 1500Z and 1700Z.",
        "Airspace restriction over area OM001 for VIP movement from 1200Z to 1600Z.",
        "Runway 18R closed for snow removal until further notice.",
        "Navigation aid VOR ABC will be under maintenance from 1000Z to 1400Z.",
        "Newly activated restricted area OM556 due to drone operations from 0800Z to 1600Z.",
        "Runway 22L temporarily closed for lighting system upgrade, expected reopening at 0200Z.",
        "Airspace closure over OM500 due to air show from 0900Z to 1200Z.",
        "Runway 05R scheduled for emergency repair between 0400Z and 0600Z."
    ]
    return [random.choice(notam_messages), random.choice(positions)]

def generate_flight_performance():
    return [random.randint(5000, 40000), random.randint(400, 500), random.choice(["Normal", "Abnormal"]), random.randint(0, 5), random.randint(100, 3000)]

def generate_aircraft_systems_status():
    systems = ["Avionics", "Hydraulics", "Electrical", "Engine", "Landing Gear"]
    statuses = ["Normal", "Warning", "Critical"]
    return [random.choice(systems), random.choice(statuses), random.choice(["No action needed", "Manual override required", "System reset needed"]), ""]

def generate_real_time_air_traffic():
    # Expanding the list of nearby aircraft with more variety
    nearby_aircraft = [
        f"AAL{random.randint(100, 999)}", f"DAL{random.randint(100, 999)}", f"UAL{random.randint(100, 999)}",
        f"JBU{random.randint(100, 999)}", f"SWA{random.randint(100, 999)}", f"BAW{random.randint(100, 999)}",
        f"AFR{random.randint(100, 999)}", f"KLM{random.randint(100, 999)}", f"Lufthansa{random.randint(100, 999)}",
        f"Emirates{random.randint(100, 999)}", f"Qantas{random.randint(100, 999)}"
    ]
    return [
        ", ".join(random.sample(nearby_aircraft, 3)),  # Select 3 random nearby aircraft
        random.randint(1, 15),  # Distance in nautical miles
        random.randint(0, 360),  # Bearing in degrees
        random.choice([
            "Maintain separation", "Climb to avoid traffic", "Turn left for traffic avoidance",
            "Descend to avoid traffic", "Increase speed to avoid traffic conflict"
        ])
    ]

def generate_waypoint_and_route_info():
    return [random.choice(positions), random.choice(positions), random.choice(["No change", "Rerouting due to traffic", "Rerouting due to weather"]), ""]

def generate_airport_operations_status():
    runways = ["09L", "09R", "27L", "27R", "13L", "13R", "18L", "18R"]
    return [random.choice(runways), random.choice(["Open", "Closed", "Under Maintenance"]), random.choice(["Low", "Moderate", "High"]), random.randint(0, 60), "Gate assigned at terminal 3"]

def generate_emergency_procedures():
    scenarios = [
        "Fire in Engine", 
        "Hydraulic Failure", 
        "Cabin Pressure Loss", 
        "Medical Emergency", 
        "Electrical Failure",
        "Smoke in Cabin", 
        "Landing Gear Failure", 
        "Mid-Air Collision Avoidance", 
        "Fuel Leak Detected", 
        "Engine Overheating",
        "Passenger Disturbance", 
        "Bird Strike", 
        "De-Pressurization", 
        "Navigation System Failure",
        "Unstable Approach Detected"
    ]
    
    steps = {
        "Fire in Engine": "Shut down affected engine, initiate fire suppression, prepare for emergency landing.",
        "Hydraulic Failure": "Switch to backup system, reduce load, prepare for manual landing.",
        "Cabin Pressure Loss": "Descend to 10,000 feet, deploy oxygen masks, contact ATC for emergency landing.",
        "Medical Emergency": "Request priority landing, notify ground medical services, continue descent.",
        "Electrical Failure": "Switch to backup power, reduce non-essential loads, prepare for landing.",
        "Smoke in Cabin": "Activate smoke removal procedure, prepare for emergency landing, notify ATC.",
        "Landing Gear Failure": "Attempt manual extension, prepare for emergency landing, conduct visual inspection if needed.",
        "Mid-Air Collision Avoidance": "Execute evasive maneuver, regain flight path, notify ATC immediately.",
        "Fuel Leak Detected": "Monitor fuel levels, declare emergency, initiate fuel dump if necessary, prepare for emergency landing.",
        "Engine Overheating": "Reduce thrust, increase airspeed for cooling, prepare for possible shutdown, notify ATC.",
        "Passenger Disturbance": "Notify cabin crew, consider diversion if disturbance persists, inform ground personnel for landing.",
        "Bird Strike": "Assess engine damage, request immediate return, prepare for possible emergency landing.",
        "De-Pressurization": "Descend to 10,000 feet, deploy oxygen masks, notify ATC for emergency landing.",
        "Navigation System Failure": "Switch to backup navigation, notify ATC, prepare for manual navigation and landing.",
        "Unstable Approach Detected": "Abort landing, execute go-around, re-align for a second attempt, notify ATC."
    }
    
    scenario = random.choice(scenarios)
    return [scenario, steps[scenario]]

def generate_cargo_and_weight_management():
    return [random.randint(50000, 250000), random.choice(["Normal", "Hazardous"]), random.choice(["Balanced", "Imbalanced"]), random.choice(["No adjustment needed", "Fuel adjustment required"])]

def generate_crew_and_passenger_status():
    return [random.choice(["Normal", "Fatigued", "Exceeded Duty Limits"]), random.choice(["Normal", "Medical Emergency", "Unruly Passenger"]), random.choice(["None", "Crew Rotation Initiated", "Emergency Landing Requested"])]

def generate_weather_predictions():
    hazards = ["Turbulence", "Thunderstorms", "Icing", "Sandstorms", "Volcanic Ash"]
    return [random.choice(hazards), random.randint(1, 5), random.choice(["Climb", "Descend", "Divert to alternate route"])]

def generate_flight_plan_monitoring():
    route_changes = ["No change", "Route deviation due to weather", "Route deviation due to traffic", "Rerouting due to technical issues", "Alternate route due to airspace closure"]
    fuel_burn_impact = random.randint(200, 1000)  # in kilograms
    clearance_status = random.choice(["Cleared", "Awaiting clearance", "Requesting clearance", "Denied clearance"])
    return [random.choice(positions), random.choice(route_changes), fuel_burn_impact, clearance_status]

def generate_satellite_communication_status():
    communication_status = random.choice(["Normal", "Intermittent", "Failed"])
    signal_strength = random.choice(["Strong", "Weak", "No Signal"])
    required_action = random.choice(["No action", "Switch to backup frequency", "Request ATC relay"])
    return [communication_status, signal_strength, required_action]

# Generate data for each dataset
current_time = start_time
while current_time <= end_time:
    # ATC Communications dataset
    atc_comm = generate_atc_communication()
    datasets["atc_communications"].append([current_time.strftime("%H:%M:%S"), call_sign] + atc_comm)
    
    # Weather dataset
    weather = generate_weather()
    datasets["weather"].append([current_time.strftime("%H:%M:%S")] + weather)
    
    # Historical Incidents dataset (generate only once in a while, simulate past incidents)
    if random.random() < 0.05:  # 5% chance of an incident
        incident = generate_historical_incidents()
        datasets["historical_incidents"].append([current_time.strftime("%Y-%m-%d")] + incident)
    
    # Flight Manuals dataset (static but relevant to certain times)
    if random.random() < 0.1:  # 10% chance of manual reference
        manual = generate_flight_manual()
        datasets["flight_manuals"].append(manual)
    
    # Fuel Management dataset
    fuel_data = generate_fuel_data()
    datasets["fuel_management"].append([current_time.strftime("%H:%M:%S"), call_sign] + fuel_data)
    
    # NOTAMs dataset
    if random.random() < 0.05:  # 5% chance of a NOTAM
        notam = generate_notam()
        datasets["notams"].append([current_time.strftime("%H:%M:%S")] + notam)

    # Flight Performance Metrics
    datasets["flight_performance"].append([current_time.strftime("%H:%M:%S"), call_sign] + generate_flight_performance())
    
    # Aircraft Systems Status
    datasets["aircraft_systems_status"].append([current_time.strftime("%H:%M:%S"), call_sign] + generate_aircraft_systems_status())
    
    # Real-Time Air Traffic
    datasets["real_time_air_traffic"].append([current_time.strftime("%H:%M:%S"), call_sign] + generate_real_time_air_traffic())
    
    # Waypoint and Route Information
    datasets["waypoint_and_route_info"].append([current_time.strftime("%H:%M:%S"), call_sign] + generate_waypoint_and_route_info())
    
    # Airport Operations Status
    datasets["airport_operations_status"].append([current_time.strftime("%H:%M:%S"), call_sign] + generate_airport_operations_status())
    
    # Emergency Procedures (these are more static and rare, so generate once in a while)
    if random.random() < 0.05:  # 5% chance of an emergency
        datasets["emergency_procedures"].append(generate_emergency_procedures())
    
    # Cargo and Weight Management
    datasets["cargo_and_weight_management"].append([current_time.strftime("%H:%M:%S"), call_sign] + generate_cargo_and_weight_management())
    
    # Crew and Passenger Status
    datasets["crew_and_passenger_status"].append([current_time.strftime("%H:%M:%S"), call_sign] + generate_crew_and_passenger_status())
    
    # Weather Predictions
    datasets["weather_predictions"].append([current_time.strftime("%H:%M:%S"), call_sign] + generate_weather_predictions())
    
    # Flight Plan Monitoring
    datasets["flight_plan_monitoring"].append([current_time.strftime("%H:%M:%S"), call_sign] + generate_flight_plan_monitoring())
    
    # Satellite Communication Status
    datasets["satellite_communication_status"].append([current_time.strftime("%H:%M:%S"), call_sign] + generate_satellite_communication_status())


    # Increment time
    current_time += time_increment

# Now write each dataset to CSV files
dataset_names = {
    "atc_communications": "atc_communications.csv",
    "weather": "weather.csv",
    "historical_incidents": "historical_incidents.csv",
    "flight_manuals": "flight_manuals.csv",
    "fuel_management": "fuel_management.csv",
    "notams": "notams.csv",
    "flight_performance": "flight_performance.csv",
    "aircraft_systems_status": "aircraft_systems_status.csv",
    "real_time_air_traffic": "real_time_air_traffic.csv",
    "waypoint_and_route_info": "waypoint_and_route_info.csv",
    "airport_operations_status": "airport_operations_status.csv",
    "emergency_procedures": "emergency_procedures.csv",
    "cargo_and_weight_management": "cargo_and_weight_management.csv",
    "crew_and_passenger_status": "crew_and_passenger_status.csv",
    "weather_predictions": "weather_predictions.csv",
    "flight_plan_monitoring": "flight_plan_monitoring.csv",
    "satellite_communication_status": "satellite_communication_status.csv"
}

for dataset_name, file_name in dataset_names.items():
    with open('../data/'+file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write headers
        if dataset_name == "atc_communications":
            writer.writerow(["Time", "Call Sign", "Communication Type", "Message Content", "Altitude (ft)", "Speed (knots)", "Heading (degrees)", "Position"])
        elif dataset_name == "weather":
            writer.writerow(["Time", "Position", "Weather Condition", "Wind Speed", "Temperature"])
        elif dataset_name == "historical_incidents":
            writer.writerow(["Date", "Incident Type", "Actions Taken", "Delay Impact (minutes)", "Remarks"])
        elif dataset_name == "flight_manuals":
            writer.writerow(["Manual Section", "Scenario", "Instructions"])
        elif dataset_name == "fuel_management":
            writer.writerow(["Time", "Call Sign", "Current Fuel (kg)", "Expected Fuel Upon Arrival (kg)", "Fuel Consumption Rate (kg/h)", "Remarks"])
        elif dataset_name == "notams":
            writer.writerow(["Time", "NOTAM", "Position"])
        elif dataset_name == "flight_performance":
            writer.writerow(["Time", "Call Sign", "Altitude (ft)", "Speed (knots)", "Engine Performance", "Deviation from Flight Path (nm)", "Fuel Efficiency (kg/hour)"])
        elif dataset_name == "aircraft_systems_status":
            writer.writerow(["Time", "Call Sign", "System", "Status", "Action Needed", "Remarks"])
        elif dataset_name == "real_time_air_traffic":
            writer.writerow(["Time", "Call Sign", "Nearby Aircraft", "Distance (nm)", "Bearing (degrees)", "ATC Instructions"])
        elif dataset_name == "waypoint_and_route_info":
            writer.writerow(["Time", "Call Sign", "Current Waypoint", "Next Waypoint", "Route Changes", "Reason for Change"])
        elif dataset_name == "airport_operations_status":
            writer.writerow(["Time", "Call Sign", "Runway", "Status", "Taxiway Congestion", "Expected Delays (minutes)", "Gate Assignment"])
        elif dataset_name == "emergency_procedures":
            writer.writerow(["Scenario", "Step-by-Step Instructions"])
        elif dataset_name == "cargo_and_weight_management":
            writer.writerow(["Time", "Call Sign", "Total Weight (kg)", "Cargo Type", "Weight Distribution", "Fuel Adjustment Needed"])
        elif dataset_name == "crew_and_passenger_status":
            writer.writerow(["Time", "Call Sign", "Crew Status", "Passenger Status", "Actions Taken"])
        elif dataset_name == "weather_predictions":
            writer.writerow(["Time", "Call Sign", "Predicted Hazard", "Time to Hazard (hours)", "Required Action"])
        elif dataset_name == "flight_plan_monitoring":
            writer.writerow(["Time", "Call Sign", "Original Route", "Updated Route", "Fuel Burn Impact (kg)", "ATC Clearance"])
        elif dataset_name == "satellite_communication_status":
            writer.writerow(["Time", "Call Sign", "Communication Status", "Signal Strength", "Required Action"])

        # Write rows
        for row in datasets[dataset_name]:
            writer.writerow(row)

