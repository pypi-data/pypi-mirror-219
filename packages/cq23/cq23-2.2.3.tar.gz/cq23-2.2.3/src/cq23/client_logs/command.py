import os
import json
from pathlib import Path


def client_names(server_log_file):
    with open(server_log_file) as f:
        # Client information is the first message send to the server, so we
        # can fetch it from there.
        for line in f:
            try:
                msg = json.loads(line)
            except ValueError:
                continue

            if "clients" in msg:
                return [client["name"] for client in msg["clients"]]


def client_log_out(client_log_file):
    log_lines = []

    with open(client_log_file) as f:
        # Skip client secret broadcast.
        next(f)

        # Bit hacky but we can filter out socket messages like this...
        msg_flag = False
        for line in f:
            if msg_flag:
                msg_flag = False
                continue

            if line.startswith(">") or line.startswith("<"):
                msg_flag = True
            else:
                log_lines.append(line)

    return log_lines


def logs(*args):
    replays_folder = os.path.join(os.getcwd(), ".game_files", "replay_files")
    server_log = list(Path(replays_folder).glob("cq_server*"))

    if not os.path.exists(replays_folder) or not server_log:
        print("No logs files available. You should first run a game: cq23 run")
        return

    names = client_names(server_log[0])

    if len(args) == 0:
        print("CLIENT NAMES")
        print("============")
        print("\n".join(names), "\n")

        print("Usage: cq23 logs <client name>")
    elif len(args) == 1:
        for i, n in enumerate(names):
            if n.lower() != args[0].lower():
                continue

            client_log = list(Path(replays_folder).glob(f"cq_client_{i}*"))

            if not client_log:
                print(f"Could not find client replay file for {args[0]}")
                return

            line = f"Logs for client: {n}"

            print(line)
            print("=" * len(line))
            print("\n".join(client_log_out(client_log[0])))

            return
    else:
        print("Usage: cq23 logs <client name>")
