from flask import Flask, request

app = Flask(__name__)

@app.route('/welcome', methods=["POST"])
def welcome():
    data = request.json
    username = data.get("name")
    return {"status":"success", "message": f'Hello, {username}!'}, 200

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8080)
