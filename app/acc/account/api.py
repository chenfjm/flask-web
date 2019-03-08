from app.acc import acc


@acc.route('/hello')
def hello_blueprint():
    return 'hello account'
