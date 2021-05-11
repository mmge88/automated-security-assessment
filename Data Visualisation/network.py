from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('interface.html')


@app.route("/security")
def security():
    return render_template('security.html')


@app.route("/path_security")
def path_security():
    return render_template('path_security.html')


@app.route("/fire_detection")
def fire_detection():
    return render_template('fire_detection.html')


@app.route("/path_fire")
def path_fire():
    return render_template('path_fire.html')


@app.route("/light")
def light():
    return render_template('light.html')


@app.route("/path_light")
def path_light():
    return render_template('path_light.html')


@app.route("/audio")
def audio():
    return render_template('audio.html')


@app.route("/path_audio")
def path_audio():
    return render_template('path_audio.html')


@app.route("/hvac")
def hvac():
    return render_template('hvac.html')


@app.route("/path_hvac")
def path_hvac():
    return render_template('path_hvac.html')


if __name__ == "__main__":
    app.run(debug=False)
