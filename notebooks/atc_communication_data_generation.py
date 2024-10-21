import pandas as pd
from datetime import datetime, timedelta
import random

# Initialize variables
call_sign = 'UAE201'
start_date = datetime.strptime('2023-10-01 00:00', '%Y-%m-%d %H:%M')
end_date = datetime.strptime('2023-10-01 23:59', '%Y-%m-%d %H:%M')

# Pre-defined communication events
communications = [
    # Pre-flight and Taxi Out
    {
        'Time': start_date + timedelta(minutes=5),
        'Phase': 'Pre-flight',
        'Frequency': '121.900',
        'Message': "UAE201, Dubai Ground, pushback and engine start approved. Expect runway 12R for departure.",
        'Altitude': 0,
        'Event_Flag': ''
    },
    {
        'Time': start_date + timedelta(minutes=10),
        'Phase': 'Taxi',
        'Frequency': '121.800',
        'Message': "UAE201, taxi to runway 12R via taxiways Alpha and Bravo. Hold short of runway 12R.",
        'Altitude': 0,
        'Event_Flag': ''
    },
    # Takeoff and Departure
    {
        'Time': start_date + timedelta(minutes=20),
        'Phase': 'Takeoff',
        'Frequency': '118.750',
        'Message': "UAE201, Dubai Tower, wind 110 degrees at 5 knots. Runway 12R cleared for takeoff.",
        'Altitude': 0,
        'Event_Flag': ''
    },
    {
        'Time': start_date + timedelta(minutes=25),
        'Phase': 'Departure',
        'Frequency': '124.500',
        'Message': "UAE201, contact Dubai Departure on 124.5. Good morning.",
        'Altitude': 3000,
        'Event_Flag': ''
    },
    # Climb
    {
        'Time': start_date + timedelta(minutes=30),
        'Phase': 'Climb',
        'Frequency': '124.500',
        'Message': "UAE201, climb and maintain flight level 150.",
        'Altitude': 10000,
        'Event_Flag': ''
    },
    {
        'Time': start_date + timedelta(minutes=40),
        'Phase': 'Climb',
        'Frequency': '127.850',
        'Message': "UAE201, proceed direct to waypoint ORLON, climb and maintain flight level 350.",
        'Altitude': 20000,
        'Event_Flag': ''
    },
    # Cruise
    {
        'Time': start_date + timedelta(hours=2),
        'Phase': 'Cruise',
        'Frequency': '132.000',
        'Message': "UAE201, maintain flight level 350, report reaching waypoint PASOV.",
        'Altitude': 35000,
        'Event_Flag': ''
    },
    # Weather Alert
    {
        'Time': start_date + timedelta(hours=4),
        'Phase': 'Cruise',
        'Frequency': '128.600',
        'Message': "UAE201, be advised of moderate turbulence ahead, suggest climb to flight level 370.",
        'Altitude': 35000,
        'Event_Flag': 'Weather Alert'
    },
    {
        'Time': start_date + timedelta(hours=4, minutes=5),
        'Phase': 'Cruise',
        'Frequency': '128.600',
        'Message': "UAE201, climb and maintain flight level 370.",
        'Altitude': 37000,
        'Event_Flag': ''
    },
    # Position Report
    {
        'Time': start_date + timedelta(hours=6),
        'Phase': 'Cruise',
        'Frequency': '125.300',
        'Message': "UAE201, report position over waypoint LALAT.",
        'Altitude': 37000,
        'Event_Flag': ''
    },
    # Descent
    {
        'Time': start_date + timedelta(hours=8),
        'Phase': 'Descent',
        'Frequency': '126.900',
        'Message': "UAE201, descend and maintain flight level 330.",
        'Altitude': 33000,
        'Event_Flag': ''
    },
    {
        'Time': start_date + timedelta(hours=9, minutes=30),
        'Phase': 'Descent',
        'Frequency': '120.300',
        'Message': "UAE201, descend and maintain 10,000 feet, reduce speed to 250 knots.",
        'Altitude': 10000,
        'Event_Flag': ''
    },
    # Approach and Landing
    {
        'Time': start_date + timedelta(hours=9, minutes=45),
        'Phase': 'Approach',
        'Frequency': '119.100',
        'Message': "UAE201, turn left heading 180 degrees, descend to 3,000 feet, cleared ILS runway 25R approach.",
        'Altitude': 3000,
        'Event_Flag': ''
    },
    {
        'Time': start_date + timedelta(hours=9, minutes=55),
        'Phase': 'Landing',
        'Frequency': '118.500',
        'Message': "UAE201, Jakarta Tower, wind 250 degrees at 10 knots, runway 25R cleared to land.",
        'Altitude': 0,
        'Event_Flag': ''
    },
    # Taxi In
    {
        'Time': start_date + timedelta(hours=10, minutes=5),
        'Phase': 'Taxi to Gate',
        'Frequency': '121.700',
        'Message': "UAE201, welcome to Jakarta, taxi to gate via taxiways Bravo and Delta.",
        'Altitude': 0,
        'Event_Flag': ''
    },
    # Ground Time
    {
        'Time': start_date + timedelta(hours=10, minutes=15),
        'Phase': 'Ground',
        'Frequency': '---',
        'Message': "-- Ground Time at Jakarta --",
        'Altitude': 0,
        'Event_Flag': ''
    },
    # Pre-flight and Taxi Out for Return Flight
    {
        'Time': start_date + timedelta(hours=14),
        'Phase': 'Pre-flight',
        'Frequency': '121.900',
        'Message': "UAE201, Jakarta Ground, pushback and start approved, expect runway 07L for departure.",
        'Altitude': 0,
        'Event_Flag': ''
    },
    {
        'Time': start_date + timedelta(hours=14, minutes=10),
        'Phase': 'Taxi',
        'Frequency': '121.800',
        'Message': "UAE201, taxi to runway 07L via taxiways Echo and Foxtrot.",
        'Altitude': 0,
        'Event_Flag': ''
    },
    # Takeoff and Departure
    {
        'Time': start_date + timedelta(hours=14, minutes=20),
        'Phase': 'Takeoff',
        'Frequency': '118.700',
        'Message': "UAE201, Jakarta Tower, wind 070 degrees at 8 knots, runway 07L cleared for takeoff.",
        'Altitude': 0,
        'Event_Flag': ''
    },
    {
        'Time': start_date + timedelta(hours=14, minutes=25),
        'Phase': 'Departure',
        'Frequency': '124.300',
        'Message': "UAE201, contact Jakarta Departure on 124.3.",
        'Altitude': 3000,
        'Event_Flag': ''
    },
    # Climb
    {
        'Time': start_date + timedelta(hours=14, minutes=30),
        'Phase': 'Climb',
        'Frequency': '124.300',
        'Message': "UAE201, climb and maintain flight level 360.",
        'Altitude': 15000,
        'Event_Flag': ''
    },
    # Emergency Situation
    {
        'Time': start_date + timedelta(hours=16),
        'Phase': 'Cruise',
        'Frequency': '125.600',
        'Message': "UAE201, we have an indication of engine failure, requesting immediate descent.",
        'Altitude': 36000,
        'Event_Flag': 'Emergency'
    },
    {
        'Time': start_date + timedelta(hours=16, minutes=5),
        'Phase': 'Descent',
        'Frequency': '125.600',
        'Message': "UAE201, roger, descend and maintain 10,000 feet, turn left heading 270 degrees, vectoring for return to Jakarta.",
        'Altitude': 10000,
        'Event_Flag': 'Emergency'
    },
    # Return and Landing after Emergency
    {
        'Time': start_date + timedelta(hours=17),
        'Phase': 'Approach',
        'Frequency': '119.100',
        'Message': "UAE201, cleared for emergency landing runway 25R, emergency services are standing by.",
        'Altitude': 3000,
        'Event_Flag': 'Emergency'
    },
    {
        'Time': start_date + timedelta(hours=17, minutes=10),
        'Phase': 'Landing',
        'Frequency': '118.500',
        'Message': "UAE201, Jakarta Tower, runway 25R cleared to land.",
        'Altitude': 0,
        'Event_Flag': 'Emergency'
    },
    # Taxi In After Emergency Landing
    {
        'Time': start_date + timedelta(hours=17, minutes=20),
        'Phase': 'Taxi to Gate',
        'Frequency': '121.700',
        'Message': "UAE201, taxi to stand, follow the escort vehicle.",
        'Altitude': 0,
        'Event_Flag': 'Emergency'
    },
    # Ground Time After Emergency
    {
        'Time': start_date + timedelta(hours=17, minutes=30),
        'Phase': 'Ground',
        'Frequency': '---',
        'Message': "-- Aircraft grounded for inspection --",
        'Altitude': 0,
        'Event_Flag': 'Emergency'
    },
]

# Create DataFrame
df = pd.DataFrame(communications)
df['call_sign'] = call_sign
# Format time
df['Time_UTC'] = df['Time'].dt.strftime('%H:%M:%S')
df = df.drop(columns=['Time'])

# Rearrange columns
df = df[['Time_UTC', 'call_sign', 'Frequency', 'Message', 'Altitude', 'Phase', 'Event_Flag']]

# Save to CSV
df.to_csv('../data/atc_communications_realistic.csv', index=False)

print("ATC communication data has been generated and saved to 'atc_communications_realistic.csv'.")
