from flask import Flask, render_template, url_for

app = Flask(__name__)
app.debug = True

@app.route('/')
def landing():
    return render_template('index.html')


app.run()