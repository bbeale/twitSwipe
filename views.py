from app import app


@app.route('/index', methods=['GET', 'POST'])
def bot():
    return 'Hello world!'
