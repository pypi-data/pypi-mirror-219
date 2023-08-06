import base64
import json
import os
import subprocess
import sys
import time
import webbrowser
from multiprocessing import Process

import requests

from cq23.web_server import flask_api

from . import docker_tools

MATCH_TIMEOUT_SECONDS = 12 * 60  # This should ideally match the one in game worker


def open_waiting_page():
    time.sleep(7)

    # Open the waiting page which redirects to the GUI
    gui_url = "https://watch.codequest.club/?base_url=http://127.0.0.1:2023/"
    base64_gui_url = base64.b64encode(gui_url.encode("utf-8")).decode("utf-8")
    loading_page_url = (
        "http://127.0.0.1:2023/F/loading_screen.html?ra=" + base64_gui_url
    )
    webbrowser.open(loading_page_url)


def run_gui():
    replay_files_directory = os.path.join(
        os.path.join(os.path.join(os.getcwd(), "gcs"), "src"), "live_replay_files"
    )
    gui_process = Process(target=flask_api.start, args=(replay_files_directory,))
    gui_process.start()

    waiting_page_process = Process(target=open_waiting_page)
    waiting_page_process.start()

    return gui_process, waiting_page_process


def stop_gui(gui_process, waiting_page_process):
    waiting_page_process.join(timeout=1)
    if waiting_page_process.is_alive():
        waiting_page_process.terminate()

    print("Requesting graceful termination of GUI server...")
    requests.request("get", "http://127.0.0.1:2023/die")

    gui_process.join(timeout=15)
    if gui_process.is_alive():
        print("Graceful termination failed, killing the GUI server...")
        gui_process.terminate()


def run_gcs(gcs_folder_name, home_image, away_image, game_map=None):
    gcs_src_dir = os.path.join(gcs_folder_name, "src")
    clients_file_content = [
        {
            "id": "1",
            "name": "Home",
            "image": home_image,
        },
        {
            "id": "2",
            "name": "Away",
            "image": away_image,
        },
    ]
    clients_file_address = "clients.json"

    with open(os.path.join(gcs_src_dir, clients_file_address), "w") as f:
        f.write(json.dumps(clients_file_content))

    subprocess_args = [
        sys.executable,
        "controller.py",
        docker_tools.get_server_image_tag(),
        clients_file_address,
    ]

    if game_map:
        subprocess_args.append("--server-arg")
        subprocess_args.append("-m " + str(game_map))

    print("Starting the game interface...")
    gui_process, waiting_page_process = run_gui()

    print("Starting the game...")
    subprocess.run(subprocess_args, timeout=MATCH_TIMEOUT_SECONDS, cwd=gcs_src_dir)
    print("Game finished.", flush=True)

    print("Stopping the game interface...")
    stop_gui(gui_process, waiting_page_process)

    os.remove(os.path.join(gcs_src_dir, clients_file_address))
