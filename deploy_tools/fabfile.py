from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = "https://github.com/26huitailang/pytdd.git"


def _create_directory_structure_if_necessary(site_folder):
    for subfoler in ("database", "static", "virtualenv", "source"):
        run("mkdir -p {}/{}".format(site_folder, subfoler))


def _get_latest_source(source_folder):
    if exists(source_folder + "/.git"):
        run("cd {} && git fetch".format(source_folder))
    else:
        run("git clone {} {}".format(REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run("cd {} && git reset --hard {}".format(source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + "/superlists/settings.py"
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, "ALLOWED_HOSTS =.+$", 'ALLOWED_HOSTS = ["{}"]'.format(site_name))
    secret_key_file = source_folder + "/superlists/secret_key.py"
    if not exists(secret_key_file):
        chars = "jkjskdfjskdjfljasidjfq2983012983012312312"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '{}'".format(key))
    append(settings_path, "\nfrom .secret_key import SECRET_KEY")


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + "/../virtualenv"
    if not exists(virtualenv_folder + "/bin/pip"):
        run("virtualenv --python=python3 {}".format(virtualenv_folder))
    run(
        "{}/bin/pip install -r {}/requirements.txt".format(
            virtualenv_folder, source_folder
        )
    )


def _update_static_files(source_folder):
    run(
        "cd {} && ../virtualenv/bin/python3 manage.py collectstatic --noinput".format(
            source_folder
        )
    )


def _update_database(source_folder):
    run(
        "cd {} && ../virtualenv/bin/python3 manage.py migrate --noinput".format(
            source_folder
        )
    )


def deploy():
    site_folder = "/home/{}/sites/{}".format(env.user, env.host)
    source_folder = site_folder + "/source"
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
