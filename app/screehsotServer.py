from flask import Flask, send_from_directory,  jsonify, request
import redis

app = Flask(__name__)
redis_client = redis.StrictRedis(host='0.0.0.0', port=80, decode_responses=True)

# Define the route to serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    # Specify the directory where your static files are located
    directory = '/path/to/your/static/files'
    
    # Use send_from_directory to send the file to the client
    return send_from_directory(directory, filename)


# Route to set data in Redis
@app.route('/set_data', methods=['POST'])
def set_data():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')

    if key and value:
        redis_client.set(key, value)
        return jsonify({'message': 'Data set successfully'}), 200
    else:
        return jsonify({'error': 'Invalid request. Key and value are required'}), 400

# Route to get data from Redis
@app.route('/get_data/<key>', methods=['GET'])
def get_data(key):
    value = redis_client.get(key)

    if value is not None:
        return jsonify({'key': key, 'value': value}), 200
    else:
        return jsonify({'error': 'Key not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
