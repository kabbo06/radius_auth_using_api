
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    username = data['username']
    password = data['password']    
    # Hardcoded authentication logic
    if username == 'user1' and password == 'pass1':
        authenticated = "ok"
        response = {'authenticated': authenticated}
        return jsonify(response)

    else:
        return Response(
        "Authentication Not Allowed!",
        status=400,
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

