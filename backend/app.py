from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS
import json
from werkzeug.utils import secure_filename

import time
import os
import random

# from gtsrb.gtsrb import *
from gtsrb.gtsrb1 import *
from gtsrb.predict import *
from Hough1 import *


app = Flask(__name__)
CORS(app)
user_request = {}

REQUESTED = 0
SUBMITTED = 1
SUCCESSES = 2
FAIL = -1


@app.route("/")
def root():
    return render_template("index.html", title="Home")


# 表单POST提交图片
@app.route('/upload/', methods=['POST'])
def upload_file():
    # print("有人访问")
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
            # print({request_id: {"user": None, "statu": REQUESTED, "time": time.time(), "pic": file, "result": None}})
            filename = request_id + "_" + secure_filename(file.filename)
            # print(filename)
            file.save(os.path.join('uploads', filename))  # file.save("./uploads/" + filename)
            predict_result = predict(filename, request_id)
            user_request[request_id] = predict_result
            result_json = json.dumps({"msg": "File uploaded successfully",
                                      "rid": request_id,
                                      "code": 10,
                                      "result": predict_result})
            print(user_request[request_id])
            return result_json, 200


def predict(filename, request_id):
    # print(os.path.join('uploads', filename))
    upload_file = cv2.imread(os.path.join('uploads', filename), cv2.IMREAD_COLOR)
    houghed_img = hough(upload_file)
    predict_result = []
    if len(houghed_img) < 1:
        predict_result.append(predict_from_file(os.path.join('uploads', filename),
                                            os.path.join("gtsrb/trained_modules1", "gtsrb1_14_1715858149.2807202-44.87744349311106_93.13539123535156%.pth")))
    else:
        for img in houghed_img:
            predict_result.append(predict_from_file(img,
                                               os.path.join("gtsrb/trained_modules1",
                                                            "gtsrb1_14_1715858149.2807202-44.87744349311106_93.13539123535156%.pth")))
    # print(user_request, predict_result)
    return predict_result


# 获得一张测试图片（临时）
@app.route('/test_img/')
def random_image():
    # 获取图片文件列表
    img_dir = "gtsrb/test_imgs"
    img_list = os.listdir(img_dir)
    # 随机选择一张图片
    img_name = random.choice(img_list)
    # 返回图片的完整路径
    # img_path = os.path.join(img_dir, img_name)
    return send_from_directory(img_dir, img_name)


# 测试
@app.route('/test', methods=['GET', 'POST', 'OPTIONS'])
def test_return():
    return json.dumps({"msg": "File uploaded successfully",
                                "rid": 2,
                                "code": 10,
                                "result": 1})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
