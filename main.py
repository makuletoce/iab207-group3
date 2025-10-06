from flask import Flask, render_template, url_for

app = Flask(__name__)
app.debug = True

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/managment')
def eventManagment():
    return render_template('event_managment.html')

@app.route('/history')
def eventHistory():
    return render_template('booking_history.html')

@app.route('/details')
def eventDetails():
    return render_template('event_details.html')


app.run()