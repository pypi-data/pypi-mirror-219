import sys

from cq23.admin.builder import command as builder
from cq23.admin.worker import command as worker
from cq23.build_image.command import build
from cq23.check.command import check
from cq23.client_logs.command import logs
from cq23.cleanup.command import cleanup
from cq23.new_client.command import new_client
from cq23.replay.command import replay
from cq23.run_game.command import run_game
from cq23.zip.command import zip

from .utils import restore_cwd


def help_message():
    message = (
        "Available commands:\n\n"
        + "> cq23 new python my_bot\n"
        + "> cq23 build <name>\n"
        + "> cq23 run\n"
        + "> cq23 run map=<map name>\n"
        + "> cq23 replay\n"
        + "> cq23 zip\n"
        + "> cq23 check\n"
        + "> cq23 logs <client name>\n"
        + "> cq23 cleanup\n\n"
        + "If you need help with the competition, post a message in Discord or email us at info@codequest.club."
    )
    print(message)


@restore_cwd
def route_command():
    command_args = sys.argv[1:]

    first_arg_mapping = {
        "new": new_client,
        "build": build,
        "run": run_game,
        "replay": replay,
        "cleanup": cleanup,
        "zip": zip,
        "check": check,
        "logs": logs,
        "worker": worker,
        "builder": builder,
    }

    if not command_args or command_args[0].lower() not in first_arg_mapping.keys():
        help_message()
    else:
        first_arg_mapping[command_args[0].lower()](*command_args[1:])
