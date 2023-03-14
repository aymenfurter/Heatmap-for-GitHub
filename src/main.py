from flask import Flask, render_template, request, send_file
from github_api import fetch_commit_data
from heatmap_generator import generate_heatmap
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        commit_data = fetch_commit_data(username)
        heatmap_image = generate_heatmap(commit_data)

        # Return the generated heatmap image as a PNG file
        img_io = BytesIO()
        heatmap_image.save(img_io, "PNG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png", as_attachment=True, attachment_filename=f"{username}_heatmap.png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
