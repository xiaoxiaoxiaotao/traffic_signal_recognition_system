from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")


# 表单POST提交图片（暂定），name="pic"，返回待定
@app.route("/pic_predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        file = request.files["pic"]
        print("file", file)
        # TODO: predict
        return 'OK'
    else:
        return render_template("pic_predict.html")


if __name__ == "__main__":
    app.run(debug=True)
