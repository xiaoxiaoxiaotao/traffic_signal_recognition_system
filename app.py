from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html", title="Home")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'picture' not in request.files:
        return 'No file part', 400
    file = request.files['picture']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        # filename = secure_filename(file.filename)
        # file.save(os.path.join('uploads', filename))
        # TODO: predict the image
        return 'File uploaded successfully', 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
