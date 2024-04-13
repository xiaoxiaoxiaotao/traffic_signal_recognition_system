from flask import Flask, render_template, request
import json
import time

app = Flask(__name__)
user_request = {}

REQUESTED = 0
SUBMITTED = 1
SUCCESSES = 2
FAIL = -1

@app.route("/")
def root():
    return render_template("index.html", title="Hello")


# 表单POST提交图片（暂定），name="pic"，返回待定
@app.route("/pic_predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        file = request.files["pic"]
        print("file", file)
        # TODO：服务端后续收到图片后，校验特征值并匹配rid
        # TODO: predict
        return 'OK'
    else:
        return render_template("pic_predict.html")


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
