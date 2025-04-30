from flask import Flask, request, jsonify, send_file
import os
import subprocess

app = Flask(__name__)

input_file = "/home/ec2-user/cortext_io/cortext_io_input/input.txt"
java_script_path = "/home/ec2-user/cortext_io/AA_cortext_io_linux_0.1/AA_cortext_io_linux/AA_cortext_io_linux_run.sh"

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

@app.route('/download-html', methods=['GET'])
def download_html():
    html_file_path = '/home/ec2-user/cortext_io/cortext_io_db/000_cortext_io.html'
    
    try:
        # Check if the file exists
        if not os.path.exists(html_file_path):
            return jsonify({
                'status': 'error',
                'message': 'HTML file not found'
            }), 404
            
        # Return the file as an attachment
        return send_file(
            html_file_path,
            mimetype='text/html',
            as_attachment=True,
            download_name='000_cortext_io.html'
        )
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/run-java', methods=['POST'])
def run_java():
    try:
        # Change to the required directory
        os.chdir('/home/ec2-user/cortext_io/AA_cortext_io_linux_0.1/AA_cortext_io_linux')

        # Run the Java script
        process = subprocess.Popen(
            [java_script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Get the output and error
        stdout, stderr = process.communicate()

        # Check if the process completed successfully
        if process.returncode == 0:
            return jsonify({
                'status': 'success',
                'message': 'Java process executed successfully',
                'output': stdout.decode('utf-8')
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Java process failed',
                'error': stderr.decode('utf-8')
            }), 500

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
