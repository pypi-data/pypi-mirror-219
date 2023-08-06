try:
    from flask import Flask, render_template
except ImportError:
    raise ImportError("flask has to be installed to run this script.")
from bokeh.embed import server_document

application = Flask(__name__)


@application.route("/")
def index():
    script = server_document(url="http://localhost:5006/pyscivis")
    return render_template("embed.html", script=script)


if __name__ == "__main__":
    application.run(port=8080)
