from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('interface.html')

# Link for security system
@app.route("/security")
def security():
    return render_template('security.html')

@app.route("/path_security")
def path_security():
    return render_template('path_security.html')

# Link for fire detection system
@app.route("/fire_detection")
def fire_detection():
    return render_template('fire_detection.html')

@app.route("/path_fire")
def path_fire():
    return render_template('path_fire.html')

# Link for lighting system
@app.route("/light")
def light():
    return render_template('light.html')

@app.route("/path_light")
def path_light():
    return render_template('path_light.html')

# Link for audiovisual system
@app.route("/audio")
def audio():
    return render_template('audio.html')

@app.route("/path_audio")
def path_audio():
    return render_template('path_audio.html')

# Link for hvac system
@app.route("/hvac")
def hvac():
    return render_template('hvac.html')

@app.route("/path_hvac")
def path_hvac():
    return render_template('path_hvac.html')

# Link for resources tracking system
@app.route("/resources")
def resources():
    return render_template('resources.html')

@app.route("/path_resources")
def path_resources():
    return render_template('path_resources.html')

# Link for maintenance system
@app.route("/maintenance")
def maintenance():
    return render_template('maintenance.html')

@app.route("/path_maintenance")
def path_maintenance():
    return render_template('path_maintenance.html')

# Link for combined security system
@app.route("/combined_security")
def combined_security():
    return render_template('combined_security.html')

@app.route("/path_combined_security")
def path_combined_security():
    return render_template('path_combined_security.html')


@app.route("/combined_ALFH")
def combined_ALFH():
    return render_template('combined_ALFH.html')

@app.route("/path_combined_ALFH")
def path_combined_ALFH():
    return render_template('path_combined_ALFH.html')


if __name__ == "__main__":
    app.run(debug=False)
