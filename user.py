from flask import jsonify, request, session
from app import mongo, bcrypt


def register():#Object of type bytes is not JSON serializable
    try:
        userdata=request.get_json()
        user = {
            "name": userdata["name"],
            "email": userdata["email"],
            "password": bcrypt.generate_password_hash(userdata["password"]),
            "is_admin": False,
        }

        if mongo.users.find_one({"email": userdata["email"]}):
            return jsonify({"message": "User already exits"}), 400
        if mongo.users.insert_one(user):
            user['_id'] = str(user['_id'])
            return jsonify(user), 200
        return jsonify({"message": "SignUp failed"}), 400

    except Exception as e:
        print(e)
        return jsonify({'message': 'SignUp failed'}), 500


def login():
    try:
        login_data=request.get_json()
        email = login_data['email']
        password = login_data['password']
        user = mongo.users.find_one({"email": email})

        if user and bcrypt.check_password_hash(user["password"], password):
            session["logged_in"] = True
            session["user"] = user
            return jsonify(user), 200
        else:
            return jsonify({"message": "Invalid login Credentials"}), 401
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal Error'}), 500


def sign_out():
    try:
        session.clear()
        return jsonify({'message': 'Signed Out'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error while signing out'}), 500
