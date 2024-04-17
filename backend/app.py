from flask import Flask, render_template, request
import json
import time
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
user_request = {}

REQUESTED = 0
SUBMITTED = 1
SUCCESSES = 2
FAIL = -1


@app.route("/")
def root():
    return render_template("index.html", title="Home")


# 表单POST提交图片
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'picture' not in request.files:
        result_json = json.dumps({"msg": "No file part", "code": 20, "result": "FAIL"})
        return result_json, 400
    file = request.files['picture']
    if file.filename == '':
        result_json = json.dumps({"msg": "No selected file", "code": 20, "result": "FAIL"})
        return result_json, 400
    if file:
        if "rid" not in request.form or request.form["rid"] == "":
            result_json = json.dumps({"msg": "No rid", "code": 20, "result": "FAIL"})
            return result_json, 400
        else:
            request_id = request.form["rid"]
            # TODO: UID
            user_request.update(
                {request_id: {"user": None, "statu": REQUESTED, "time": time.time(), "pic": file, "result": None}})
            # filename = secure_filename(file.filename)
            print(os.path.join('uploads'))
            # file.save(os.path.join('uploads', filename))
            # TODO: predict the image, and give results

            print(user_request)
            result_json = json.dumps({"msg": "File uploaded successfully", "rid": request_id, "code": 10, "result": "AAAAAA"})
            return result_json, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
