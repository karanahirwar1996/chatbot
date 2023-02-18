from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data['message']
    response = f"Hello, {message}!"
    return {'response': response}
