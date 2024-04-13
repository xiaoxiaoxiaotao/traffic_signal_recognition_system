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


# 表单POST提交图片（暂定），name="pic"，返回待定
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



@app.route("/pic_predict/pass_info", methods=["POST"])
def before_predict():
    data = request.form
    print(data)
    user_id = data["uid"]
    request_id = data["rid"]  # rid用户生成，采用图片hash
    user_request.update({request_id: {"user": user_id, "statu": REQUESTED, "time": time.time(), "pic": None, "result": None}})
    print(user_request)
    result_json = json.dumps({"code": 200, "data": {"uid": user_id, "rid": request_id}})
    return result_json


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
