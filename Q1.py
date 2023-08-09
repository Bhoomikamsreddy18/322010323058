from flask import Flask, jsonify
import requests
import datetime

app = Flask(__name__)

# Configuration
BASE_URL = "http://20.244.56.144/train"
CLIENT_ID = "b46118f0-fbde-4b16-a4b1-6ae6ad718b27"
CLIENT_SECRET = "XOyolORPasKWOdAN"


@app.route('/trains', methods=['GET'])
def get_trains():
    try:
        get_authorization_token()
        train_data = fetch_train_data()
        if not train_data:
            return "No train data available."

        # Process and filter train data
        filtered_trains = process_train_data(train_data)

        # Sort trains based on criteria
        sorted_trains = sort_trains(filtered_trains)

        return jsonify(sorted_trains)

    except Exception as e:
        print("Error:", str(e))
        return "error occurred."


def get_authorization_token():
    try:
        url = "{BASE_URL}/auth"
        data = {
            "companyName": "Train Central",
            "clientID": CLIENT_ID,
            "ownerName": "Rahul",
            "ownerEmail": "rahul@abc.edu",
            "rollNo": "1",
            "clientSecret": CLIENT_SECRET
        }
        response = requests.post(url, json=data)
        response_json = response.json()
        token = response_json.get("access_token")
        return token

    except Exception as e:
        print("Authorization Error:", str(e))
        return None


def fetch_train_data():
    try:
        headers = {"Authorization": "Bearer {auth_token}"}
        url = "{BASE_URL}/trains"
        response = requests.get(url, headers=headers)
        response_json = response.json()
        return response_json

    except Exception as e:
        print("Train Data Fetch Error:", str(e))
        return []


def process_train_data(train_data):
    try:
        now = datetime.datetime.now()
        filtered_trains = []

        for train in train_data:
            if "departureTime" in train and isinstance(train["departureTime"], dict):
                departure_time = datetime.datetime(
                    now.year, now.month, now.day,
                    train["departureTime"]["Hours"],
                    train["departureTime"]["Minutes"],
                    train["departureTime"]["Seconds"]
                )
                delayed_by = train.get("delayedBy", 0)
                departure_time += datetime.timedelta(minutes=delayed_by)

                if departure_time > now + datetime.timedelta(minutes=30):
                    train["actualDepartureTime"] = departure_time.strftime("%H:%M:%S")
                    filtered_trains.append(train)
            else:
                print("Train data structure error:", train)

        return filtered_trains

    except Exception as e:
        print("Train Data Processing Error:", str(e))
        return []


def sort_trains(trains):
    try:
        sorted_trains = sorted(
            trains,
            key=lambda x: (
            x["price"]["sleeper"], x["price"]["AC"], -x["seatsAvailable"]["sleeper"], -x["seatsAvailable"]["AC"],
            -datetime.datetime.strptime(x["actualDepartureTime"], "%H:%M:%S").timestamp())
        )
        return sorted_trains

    except Exception as e:
        print("Sorting Error:", str(e))
        return []


if __name__ == '__main__':
    app.run(debug=True)
