from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///activities.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)
    head_of_department = db.Column(db.String(100), nullable=False)
    activity_name = db.Column(db.String(200), nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in days
    status = db.Column(db.String(10), nullable=False)  # 'On Time' or 'Overdue'

    def __repr__(self):
        return f'<Activity {self.activity_name}>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_activity():
    if request.method == 'POST':
        department_name = request.form['department_name']
        head_of_department = request.form['head_of_department']
        activity_name = request.form['activity_name']
        scheduled_date = datetime.strptime(request.form['scheduled_date'], '%Y-%m-%d')
        duration = int(request.form['duration'])
        status = 'On Time' if scheduled_date >= datetime.now() else 'Overdue'

        new_activity = Activity(department_name=department_name, head_of_department=head_of_department,
                                activity_name=activity_name, scheduled_date=scheduled_date, 
                                duration=duration, status=status)

        try:
            db.session.add(new_activity)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return 'There was an issue adding your activity'

    return render_template('add_activity.html')

@app.route('/activities')
def view_activities():
    try:
        activities = Activity.query.order_by(Activity.scheduled_date).all()
        return render_template('view_activities.html', activities=activities)
    except Exception as e:
        print(e)
        return 'There was an issue retrieving activities'

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()  # Drop all tables
        db.create_all()  # Create tables with the updated schema
    app.run(host='0.0.0.0', port=5000, debug=True)
