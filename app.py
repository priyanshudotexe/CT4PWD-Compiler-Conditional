from flask import Flask, request, jsonify
import cv2
import pytesseract
import os
from werkzeug.utils import secure_filename
import color_extractor
import lex
import parse
import eval

# Import your existing modules

app = Flask(__name__)

@app.route('/helloworld', methods=['GET'])
def helloworld():
    return jsonify({"message": "helloworld"}), 200

@app.route('/compile', methods=['POST'])
def compile_image():
    try:

        # Check if image_path is provided in the form data
        image_path = request.form.get('image_path')
        print(f"[DEBUG] Received image_path: {image_path}")
        if image_path:
            filepath = image_path
            print(f"[DEBUG] File exists: {os.path.exists(filepath)}")
        else:
            # Check if the file is in the request
            if 'file' not in request.files:
                print("[DEBUG] No file part in the request and no image_path provided")
                return jsonify({"error": "No file part in the request and no image_path provided"}), 400

            file = request.files['file']

            # Check if a file was uploaded
            if file.filename == '':
                print("[DEBUG] No file selected for uploading")
                return jsonify({"error": "No file selected for uploading"}), 400

            # Save the uploaded file as uploaded.png
            filename = secure_filename("uploaded.png")
            filepath = os.path.join(os.getcwd(), filename)
            file.save(filepath)
            print(f"[DEBUG] Uploaded file saved to: {filepath}")


         # Delegate image processing to tempCodeRunnerFile.py
        import subprocess
        import sys
        try:
            # Determine the correct Python executable
            # Try different possible Python executables in order of preference
            possible_pythons = [
                os.path.join(os.getcwd(), 'env', 'Scripts', 'python.exe'),  # Windows venv
                os.path.join(os.getcwd(), 'env', 'bin', 'python'),          # Linux venv
                sys.executable,                                              # Current Python
                'python3',                                                   # System python3
                'python'                                                     # System python
            ]
            
            python_executable = None
            for python_path in possible_pythons:
                if os.path.isfile(python_path) and os.access(python_path, os.X_OK):
                    python_executable = python_path
                    break
                elif python_path in ['python3', 'python']:
                    # For system commands, check if they exist
                    try:
                        subprocess.run([python_path, '--version'], capture_output=True, check=True)
                        python_executable = python_path
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
            
            if python_executable is None:
                return jsonify({"error": "No suitable Python executable found"}), 500
            
            print(f"[DEBUG] Using Python executable: {python_executable}")
            result = subprocess.run([
                python_executable,
                os.path.join(os.getcwd(), 'tempCodeRunnerFile.py'),
                filepath
            ], capture_output=True, text=True, check=True)
            output = result.stdout
            print(f"[DEBUG] tempCodeRunnerFile.py output:\n{output}")
            # Extract the final output from the script's output
            # Look for the line starting with 'Final Output:'
            final_output = None
            for line in output.splitlines():
                if line.startswith('Final Output:'):
                    # The next line should be the actual output
                    idx = output.splitlines().index(line)
                    if idx + 1 < len(output.splitlines()):
                        final_output = output.splitlines()[idx + 1]
                    break
            if final_output is None:
                return jsonify({"error": "No final output found in tempCodeRunnerFile.py response.", "raw_output": output}), 500
            return jsonify({"output": final_output}), 200
        except subprocess.CalledProcessError as e:
            print(f"[DEBUG] tempCodeRunnerFile.py failed: {e}")
            return jsonify({"error": "tempCodeRunnerFile.py failed", "details": e.stderr}), 500

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)