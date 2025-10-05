from flask import Flask, render_template, url_for

app = Flask(__name__)
app.debug = True

@app.route('/')
def landing():
    return render_template('index_dynamic.html')

@app.route('/managment')
def eventManagment():
    return render_template('event_d_managment.html')

@app.route('/history')
def eventHistory():
    return render_template('booking-history.html')


app.run()