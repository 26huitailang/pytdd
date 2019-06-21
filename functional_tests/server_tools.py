from os import path
import subprocess

THIS_FOLDER = path.dirname(path.abspath(__file__))


def _replace_local_vbox_port():
    return "127.0.0.1:2222"


def reset_database(host):
    host = _replace_local_vbox_port()
    subprocess.check_call(
        ["fab", "reset_database", "--host=vagrant@{}".format(host)], cwd=THIS_FOLDER
    )


def create_session_on_server(host, email):
    host = _replace_local_vbox_port()
    return (
        subprocess.check_output(
            [
                "fab",
                "create_session_on_server:email={}".format(email),
                "--host=vagrant@{}".format(host),
                "--hide=everything,status",
            ],
            cwd=THIS_FOLDER,
        )
        .decode()
        .strip()
    )
