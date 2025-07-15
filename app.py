from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret"  # You can use a more secure key in production

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pomodoro.db'
db = SQLAlchemy(app)

# Pomodoro session model
class PomodoroSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create DB tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    total_sessions = PomodoroSession.query.count()
    return render_template('index.html', completed=total_sessions)

@app.route('/complete')
def complete_session():
    new_session = PomodoroSession()
    db.session.add(new_session)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/history')
def history():
    sessions = PomodoroSession.query.order_by(PomodoroSession.completed_at.desc()).all()
    return render_template('history.html', sessions=sessions)

# ✅ Run the app on all interfaces (important for Jenkins)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
