from flask import Flask, render_template, request
import json
import time
from werkzeug.utils import secure_filename
import os

from gtsrb.predict import *


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
            # TODO: Let user_request update with the filename rather than the file object.
            # TODO: No same rid
            # TODO: UID
            user_request.update(
                {request_id: {"user": None, "statu": REQUESTED, "time": time.time(), "pic": file, "result": None}})
            filename = request_id + "_" + secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))  # file.save("./uploads/" + filename)
            predict_result = predict_from_file(os.path.join('uploads', filename),
                                               os.path.join("gtsrb/trained_modules", "gtsrb_1906.pth"))
            print(user_request, predict_result)
            result_json = json.dumps({"msg": "File uploaded successfully",
                                      "rid": request_id,
                                      "code": 10,
                                      "result": predict_result})
            return result_json, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
