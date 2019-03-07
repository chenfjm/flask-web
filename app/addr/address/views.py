from app.addr import addr


@addr.route('/hello')
def hello_blueprint():
    return 'hello address'
