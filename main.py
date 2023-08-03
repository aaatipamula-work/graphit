from hashlib import sha256
from os.path import join, exists
from json import dumps

from flask import Flask, request, url_for, send_file, redirect
import matplotlib
from matplotlib import pyplot as plot

matplotlib.use('agg')
app = Flask(__name__)


# Generate a unique hash string based on some JSON/dictionary
def generate_hash(data: dict):
    normalized = dumps(data, separators=(',', ':'))
    return sha256(bytes(normalized, encoding="utf-8")).hexdigest()


def generate_image(data: dict, image_hash: str):
    """Generate an image and save it"""

    # Grab the actual data
    groups = data["columns"].keys()
    values = data["columns"].values()

    # Format graph
    plot.title(data["chart_title"])
    if data["type"] == "bar":
        plot.bar(groups, values, color="royalblue", width=0.4)
        plot.xlabel(data["x_axis"])
        plot.ylabel(data["y_axis"])
    elif data["type"] == "pie":
        ax = plot.subplot()
        ax.pie(values, labels=groups, autopct="%1.1f%%")

    # Save image
    save_file = join("static", image_hash + ".png")
    plot.savefig(save_file)
    plot.close("all")


@app.get("/blob/image/<graphid>")
def return_image(graphid):
    image_file = join("static", graphid + ".png")
    if exists(image_file):
        return send_file(image_file, mimetype="image/png")
    return {"error": "Image does not exist"}, 404


@app.post("/api/generate/graph")
def redirect_graph_uri():
    if not request.is_json:
        return 400
    data = request.json
    image_hash = generate_hash(data)

    # If a similar request already generated an image
    if exists(join("static", image_hash + ".png")):
        return redirect(url_for('return_image', graphid=image_hash))

    # Try and generate an image
    try:
        generate_image(data, image_hash)
    except Exception as e:
        return {"error": str(e)}, 400
    return redirect(url_for('return_image', graphid=image_hash))
