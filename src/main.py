from flask import Flask, render_template, request, send_file
import io
import os 
from github_api import fetch_hourly_commits
from heatmap_generator import generate_heatmap

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"))
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        commit_data = fetch_hourly_commits(username)
        heatmap_image = generate_heatmap(commit_data)

        img_io = io.BytesIO()
        heatmap_image.savefig(img_io, format="PNG", bbox_inches="tight")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
