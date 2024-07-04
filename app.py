from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise TEXT NOT NULL,
        duration INTEGER NOT NULL,
        date TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal TEXT NOT NULL,
        target_date TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_workout', methods=['GET', 'POST'])
def record_workout():
    if request.method == 'POST':
        exercise = request.form['exercise']
        duration = request.form['duration']
        date = request.form['date']
        conn = sqlite3.connect('fitness.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO workouts (exercise, duration, date) VALUES (?, ?, ?)', (exercise, duration, date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('record_workout.html')

@app.route('/set_goals', methods=['GET', 'POST'])
def set_goals():
    if request.method == 'POST':
        goal = request.form['goal']
        target_date = request.form['target_date']
        conn = sqlite3.connect('fitness.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO goals (goal, target_date) VALUES (?, ?)', (goal, target_date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('set_goals.html')

@app.route('/view_progress')
def view_progress():
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workouts')
    workouts = cursor.fetchall()
    cursor.execute('SELECT * FROM goals')
    goals = cursor.fetchall()
    conn.close()
    return render_template('view_progress.html', workouts=workouts, goals=goals)

@app.route('/add_sample_data')
def add_sample_data():
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO workouts (exercise, duration, date) VALUES (?, ?, ?)', ('Running', 30, '2024-06-30'))
    cursor.execute('INSERT INTO goals (goal, target_date) VALUES (?, ?)', ('Run 5km', '2024-07-15'))
    conn.commit()
    conn.close()
    return redirect(url_for('view_progress'))

if __name__ == '__main__':
    app.run(debug=True)
