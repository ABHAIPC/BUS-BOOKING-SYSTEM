from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.models import db, Bus, Route, Schedule, Passenger, Reservation, Payment, Driver, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bus_reservation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Replace with a random secret key
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        user = User.query.get(user_id)
        if not user or not getattr(user, 'IsAdmin', False):
            flash('Access Denied. Admins only.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    current_user = None
    if user_id:
        current_user = User.query.get(user_id)
    return dict(current_user=current_user)

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(Username=username).first()
        if user and check_password_hash(user.Password, password):
            session['user_id'] = user.User_ID
            flash('Login successful!', 'success')
            return redirect(url_for('get_ticket'))  # Redirect to get ticket page
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

# Sign-in page route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)  # Removed method='sha256' for compatibility

        if User.query.filter_by(Username=username).first():
            flash('Username already exists!', 'danger')
        else:
            is_admin = True if username.lower() == 'admin' else False
            new_user = User(Username=username, Password=hashed_password, IsAdmin=is_admin)
            db.session.add(new_user)
            db.session.commit()
            flash('Sign-in successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signin.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out securely. // CONNECTION_TERMINATED', 'success')
    return redirect(url_for('login'))

# Get ticket page route
@app.route('/getticket', methods=['GET', 'POST'])
def get_ticket():
    if request.method == 'POST':
        selected_route_id = request.form['route']  # Get selected route from form
        travel_date = request.form['travel_date']
        return redirect(url_for('schedules', route_id=selected_route_id, travel_date=travel_date))
    
    routes = Route.query.all()  # Get all available routes
    return render_template('getticket.html', routes=routes)

# Schedule page route
@app.route('/schedules')
def schedules():
    route_id = request.args.get('route_id')
    travel_date = request.args.get('travel_date')

    schedules = Schedule.query.filter(Schedule.Route_ID == route_id).all()  # Get schedules based on selected route

    return render_template('schedules.html', schedules=schedules, travel_date=travel_date)


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    user = User.query.get(session.get('user_id'))
    return render_template('admin_dashboard.html', user=user)

@app.route('/admin/add_route', methods=['GET', 'POST'])
@admin_required
def addroute():
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        distance = request.form['distance']
        estimated_travel_time_str = request.form['estimated_travel_time']
        
        # Convert string to datetime.time object
        try:
            estimated_travel_time = datetime.strptime(estimated_travel_time_str, '%H:%M:%S').time()
        except ValueError:
            estimated_travel_time = datetime.strptime(estimated_travel_time_str, '%H:%M').time()

        new_route = Route(Source=source, Destination=destination, Distance=distance, Estimated_Travel_Time=estimated_travel_time)
        db.session.add(new_route)
        db.session.commit()
        
        flash('Route added successfully!', 'success')
        return redirect(url_for('addroute'))

    return render_template('add_route.html')  # Render the form on GET


@app.route('/admin/add_schedule', methods=['GET', 'POST'])
@admin_required
def addschedule():
    if request.method == 'POST':
        bus_id = request.form['bus_id']
        route_id = request.form['route_id']
        departure_time_str = request.form['departure_time']
        arrival_time_str = request.form['arrival_time']

        try:
            departure_time = datetime.strptime(departure_time_str, '%Y-%m-%dT%H:%M')
            arrival_time = datetime.strptime(arrival_time_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            departure_time = datetime.strptime(departure_time_str, '%Y-%m-%d %H:%M:%S')
            arrival_time = datetime.strptime(arrival_time_str, '%Y-%m-%d %H:%M:%S')

        new_schedule = Schedule(Bus_ID=bus_id, Route_ID=route_id, Departure_Time=departure_time, Arrival_Time=arrival_time)
        db.session.add(new_schedule)
        db.session.commit()

        flash('Schedule added successfully!', 'success')
        return redirect(url_for('addschedule'))

    return render_template('addschedule.html')  # Render the form on GET

@app.errorhandler(404)
def not_found_error(error):
    return "404 Error: Page not found", 404


@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)  # Fetch user by ID
        return render_template('dashboard.html', user=user)  # Pass user data to the template
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))
    
@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
  
    if request.method == 'POST':
        # Get schedule ID from form submission
        schedule_id = request.form['schedule_id']
        
        # If passenger information is being submitted (after selecting a schedule)
        if 'name' in request.form:
            name = request.form['name']
            gender = request.form['gender']
            age = request.form['age']
            contact_number = request.form['contact_number']
            email = request.form['email']

            # Check if the passenger already exists
            passenger = Passenger.query.filter_by(Email=email).first()
            if not passenger:
                passenger = Passenger(Name=name, Gender=gender, Age=age, Contact_Number=contact_number, Email=email)
                db.session.add(passenger)
                db.session.commit()

            seat_number = request.form['seat_number']

            # Create a new reservation
            new_reservation = Reservation(
                Passenger_ID=passenger.Passenger_ID,
                Schedule_ID=schedule_id,
                Seat_Number=seat_number,
                Reservation_Date=datetime.now(),
                Status='Confirmed'
            )
            db.session.add(new_reservation)
            db.session.commit()

            flash('Ticket booked successfully!', 'success')
            return redirect(url_for('book_ticket'))

        # Render the booking form with the schedule information
        schedule = Schedule.query.get(schedule_id)
        return render_template('book_ticket.html', schedule=schedule)

    return render_template('book_ticket.html')


if __name__ == '__main__':
    app.run(debug=True)
