# add_multiple_schedules.py

from app import app, db # Adjust the import according to your app structure
from models.models import Schedule
from datetime import datetime

# Define the schedules to be added
schedules_to_add = [
    {
        'Bus_ID': 1,
        'Route_ID': 1,  # Adjust according to your existing routes
        'Departure_Time': datetime(2024, 10, 20, 10, 0),  # Example departure time
        'Arrival_Time': datetime(2024, 10, 20, 12, 0)     # Example arrival time
    },
    {
        'Bus_ID': 1,
        'Route_ID': 1,
        'Departure_Time': datetime(2024, 10, 21, 9, 0),  # Different departure time
        'Arrival_Time': datetime(2024, 10, 21, 11, 0)
    },
    {
        'Bus_ID': 2,
        'Route_ID': 1,
        'Departure_Time': datetime(2024, 10, 22, 8, 30),  # Example with another bus
        'Arrival_Time': datetime(2024, 10, 22, 10, 30)
    },
]

# Use the application context to access the database
with app.app_context():
    for schedule in schedules_to_add:
        new_schedule = Schedule(
            Bus_ID=schedule['Bus_ID'],
            Route_ID=schedule['Route_ID'],
            Departure_Time=schedule['Departure_Time'],
            Arrival_Time=schedule['Arrival_Time']
        )
        db.session.add(new_schedule)

    # Commit the changes to the database
    try:
        db.session.commit()
        print('Schedules added successfully!')
    except Exception as e:
        db.session.rollback()  # Rollback if there's an error
        print('Error adding schedules:', str(e))
