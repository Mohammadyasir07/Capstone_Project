from flask import Flask
from flask import render_template
from flask import Response
from flask import jsonify

from detector import generate_frames
from detector import people_count

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/count")
def count():
    from detector import people_count
    return jsonify({"count":people_count})


if __name__=="__main__":
    app.run(debug=True)

