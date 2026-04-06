# add_routes.py

from app import app, db
from models.models import Route
from datetime import time

# Use the application context to access the database
with app.app_context():
    # Delete existing routes (optional: you can specify conditions to avoid deleting everything)
    db.session.query(Route).delete()  # Deletes all existing routes
    db.session.commit()  # Commit deletion

    # Define multiple routes to be added
    routes_to_add = [
        {
            'Source': 'KANNUR',
            'Destination': 'KOCHI',
            'Distance': 270.0,
            'Estimated_Travel_Time': time(5, 0)
        },
        {
            'Source': 'KANNUR',
            'Destination': 'THIRUVANANTHAPURAM',
            'Distance': 300.0,
            'Estimated_Travel_Time': time(6, 0)
        },
        {
            'Source': 'KOCHI',
            'Destination': 'KOTTAYAM',
            'Distance': 160.0,
            'Estimated_Travel_Time': time(3, 0)
        },
    ]

    # Add new routes
    for route_data in routes_to_add:
        new_route = Route(
            Source=route_data['Source'],
            Destination=route_data['Destination'],
            Distance=route_data['Distance'],
            Estimated_Travel_Time=route_data['Estimated_Travel_Time']
        )
        db.session.add(new_route)

    # Commit the changes to the database for all routes
    try:
        db.session.commit()
        print('Routes added successfully!')
    except Exception as e:
        db.session.rollback()  # Rollback if there's an error
        print('Error adding routes:', str(e))
