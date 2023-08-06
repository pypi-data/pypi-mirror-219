import os
import time
import webbrowser
from multiprocessing import Process

import requests

from cq23.web_server import flask_api


def run_gui(replay_files_directory):
    gui_process = Process(target=flask_api.start, args=(replay_files_directory,))
    gui_process.start()
    webbrowser.open("https://watch.codequest.club/?base_url=http://127.0.0.1:2023/")
    return gui_process


def stop_gui(gui_process):
    print("Requesting graceful termination of GUI server...")
    requests.request("get", "http://127.0.0.1:2023/die")

    gui_process.join(timeout=60)
    if gui_process.is_alive():
        print("Graceful termination failed, killing the GUI server...")
        gui_process.terminate()


def replay(*args):
    if not args:
        replays_folder = os.path.join(
            os.getcwd(), os.path.join(".game_files", "replay_files")
        )
        if not os.path.exists(replays_folder):
            print("No replay files available. You should first run a game: cq23 run")
            return
        process = run_gui(replays_folder)
        time.sleep(1)
        stop_gui(process)
    else:
        match_id = args[0]
        if not str(match_id).isnumeric():
            print("Match id should be a number: cq23 replay 123")
            return
        webbrowser.open(
            f"https://watch.codequest.club/?base_url=api.codequest.club/api/matches/{match_id}/"
        )
