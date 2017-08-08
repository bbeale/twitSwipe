from app import app

@app.route("/index" methods=["GET", "POST"])
def pot_bot():
    return "Hello world!"