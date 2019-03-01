from app.pay import pay


@pay.route("/hello")
def hello_blueprint():
    return "hello pay weixin!"
