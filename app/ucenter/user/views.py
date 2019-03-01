from app.ucenter import uc


@uc.route("/hello")
def hello_blueprint():
    return "hello blueprint!"
