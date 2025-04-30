from flask import Flask, request, jsonify
import os

app = Flask(__name__)

input_file = "/home/ec2-user/cortext_io/cortext_io_input/input.txt"

@app.route('/write', methods=['POST'])
def write_to_file():
    data = request.json

    if not data or 'text' not in data:
        return jsonify({'status': 'error', 'message': 'No text provided'}), 400

    text = data['text']

    try:
        with open(input_file, 'w') as file:
            file.write(text)
        return jsonify({'status': 'success', 'message': 'Text written to file'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
