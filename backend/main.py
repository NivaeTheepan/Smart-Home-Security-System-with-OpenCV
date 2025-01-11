from camera import Camera  # Custom module for camera handling
from notifications import send_notification  # Function to send notifications
from storage import list_videos_in_date_range  # Function to fetch videos from storage
from flask_cors import CORS  # Enables Cross-Origin Resource Sharing
from flask import Flask, jsonify, request  # Flask components for API and requests
from datetime import datetime  # For working with date and time

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Initialize the camera system
camera = Camera()

@app.route('/arm', methods=['POST'])
def arm():
    #API endpoint to arm the camera system.
    camera.arm()
    return jsonify(message="System armed."), 200

@app.route('/disarm', methods=['POST'])
def disarm():
    #API endpoint to disarm the camera system.
    camera.disarm()
    return jsonify(message="System disarmed."), 200

@app.route('/get-armed', methods=['GET'])
def get_armed():
    #API endpoint to check if the system is armed.
    return jsonify(armed=camera.armed), 200

@app.route('/motion_detected', methods=['POST'])
def motion_detected():
    #API endpoint triggered when motion is detected.
    #Expects a JSON payload with a 'url' key.
    data = request.get_json()
    if 'url' in data:
        print("URL received:", data['url'])
        send_notification(data["url"])
    else:
        print("'url' not in incoming data")

    return jsonify({}), 201

@app.route("/get-logs")
def get_logs():
    #API endpoint to fetch logs of videos within a specified date range.
    #Expects 'startDate' and 'endDate' as query parameters in 'yyyy-mm-dd' format.
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")

    # Validate date format
    try:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use yyyy-mm-dd."}), 400

    logs = list_videos_in_date_range(start_date, end_date)
    print(f"Logs returned: {logs}")  # Debugging
    return jsonify({"logs": logs}), 200

if __name__ == "__main__":
    # Run the Flask app on all network interfaces, port 5000
    app.run(host='0.0.0.0', port=5000)
