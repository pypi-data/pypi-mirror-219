import logging
import os
import time
from threading import Thread

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from werkzeug.serving import make_server

app = Flask(__name__, static_url_path="/F", static_folder="files")
CORS(app)
ROOT_DIRECTORY = None
PORT = None
LAST_REQUEST_TIME = time.time()
SERVER = None


def get_full_path_or_404(file_name):
    full_file_path = os.path.join(ROOT_DIRECTORY, file_name)
    if not os.path.exists(full_file_path):
        return False, (jsonify({"message": "Replay file not found."}), 404)

    return True, full_file_path


def check_death_timer():
    while True:
        if time.time() - LAST_REQUEST_TIME > 3:
            print("GUI server shutting down...")
            SERVER.shutdown()
            break
        time.sleep(1)  # Check every second


@app.after_request
def after_request(response):
    global LAST_REQUEST_TIME
    LAST_REQUEST_TIME = time.time()

    response.headers[
        "Cache-Control"
    ] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def heartbeat():
    return "I'm up"


@app.route("/die", methods=["GET"])
def die():
    death_thread = Thread(target=check_death_timer)
    death_thread.start()
    return "OK"


@app.route("/download_file", methods=["GET"])
def download_file():
    assert ROOT_DIRECTORY
    file_name = request.args["file_name"]
    valid, response = get_full_path_or_404(file_name)
    if not valid:
        return response
    return send_file(response)


@app.route("/get_replay_file_url", methods=["GET"])
def get_file_url():
    assert ROOT_DIRECTORY and PORT
    file_name = request.args["file_name"]

    valid, response = get_full_path_or_404(file_name)
    if not valid:
        return response

    return jsonify(
        {
            "message": "ok",
            "url": f"http://127.0.0.1:{PORT}/download_file?file_name={file_name}",
        }
    )


@app.route("/get_replay_file_content", methods=["GET"])
def get_file_contents():
    assert ROOT_DIRECTORY
    file_name = request.args["file_name"]

    valid, response = get_full_path_or_404(file_name)
    if not valid:
        return response

    with open(response) as f:
        file_content = f.read()

    return jsonify({"message": "ok", "content": file_content})


def start(replay_files_directory, port=2023, debug=False):
    if not debug:
        logging.getLogger("werkzeug").setLevel(logging.ERROR)

    global ROOT_DIRECTORY, PORT
    ROOT_DIRECTORY = replay_files_directory
    PORT = port

    global SERVER
    SERVER = make_server("0.0.0.0", port, app, threaded=True)
    SERVER.serve_forever()
    # app.run(debug=debug, port=PORT, threaded=True)
