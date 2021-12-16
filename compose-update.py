import os
import click
import sys
import select
import subprocess
import logging
import multiprocessing as mp

logging.basicConfig(level=logging.INFO, format='%(message)s')

OKGREEN = '\033[92m'
ENDC = '\033[0m'


def color(x):
    return f"{OKGREEN}{x}{ENDC}"


def get_stdin():
    stdin = ""
    if select.select([sys.stdin, ], [], [], 0.0)[0]:
        stdin = sys.stdin.read().splitlines()
    return stdin


class FilesDefaultToStdin(click.Argument):
    def __init__(self, *args, **kwargs):
        kwargs['nargs'] = -1
        super().__init__(*args, **kwargs)

    def full_process_value(self, ctx, value):
        return super().process_value(ctx, value or get_stdin())


@click.command()
@click.option('--prune/--no-prune', default=False, help="Prune docker images after update process if set")
@click.argument('update_dirs', cls=FilesDefaultToStdin)
def update_composes(update_dirs, prune=False):
    """
    Update docker-compose images automaticly. 

    Takes one or more directorys as input and searches for a compose file in one of the following forms:
    "compose.yaml",
    "compose.yml",
    "docker-compose.yaml",
    "docker-compose.yml"
    """
    update_dirs_set = set(update_dirs)

    logging.info(
        f"Starting update process on '{len(update_dirs_set)}' compose stacks")
    logging.info(
        color("Checking directory paths and searching for compose files."))

    compose_calls = [['docker', 'compose'],
                     ['docker-compose']]

    # find a matching call for docker compose
    for compose_call in compose_calls:
        compose_prefix = None
        with open(os.devnull, 'wb') as devnull:
            try:
                subprocess.check_call(['docker', 'compose'],
                                      stdout=devnull, stderr=subprocess.STDOUT)
                compose_prefix = ' '.join(compose_call)
                break
            except subprocess.CalledProcessError:
                logging.debug(
                    f"Checked '{compose_call}' it is not an executable")
    if not compose_prefix:
        raise Exception("Couldn't find a docker compose executable.")

    compose_names = {"compose.yaml",
                     "compose.yml",
                     "docker-compose.yaml",
                     "docker-compose.yml"}

    compose_paths = []
    for update_dir in update_dirs_set:
        try:
            # check if dir exist
            if not os.path.isdir(update_dir):
                raise NotADirectoryError(f"'{update_dir}'")
            # check if dir contains compose file
            compose_file = compose_names.intersection(os.listdir(update_dir))
            if len(compose_file) == 0:
                raise FileNotFoundError(
                    f"Directory '{update_dir}' doesn't contain a compose file in one of the following forms: {compose_names}")
            if len(compose_file) > 1:
                raise Exception(
                    f"Directory '{update_dir}' contains more then one compose file, namely: {compose_file}")
            compose_paths.append(os.path.join(update_dir, compose_file.pop()))
        except Exception as e:
            logging.warning(e)

    with mp.Pool(mp.cpu_count()) as pool:
        logging.info(color("Pulling images"))

        def pull_images(compose_path):
            return subprocess.call([compose_prefix, "-f", compose_path, "pull", "--quiet"])
        results = pool.map(pull_images, compose_paths)

        # filter compose_paths where pulling finished succesfully
        finished = [idx for idx, result in enumerate(results) if result == 0]
        filtered_compose_paths = [compose_path for idx, compose_path in enumerate(
            compose_paths) if idx in finished]

        logging.info(color("Restarting composes"))

        def update_compose(compose_path):
            return os.system(f'{compose_prefix} -f {compose_path} up -d')
        results = pool.map(update_compose, filtered_compose_paths)

    logging.info(
        f"Update process finished on {results.count(0)}/{len(update_dirs_set)} compose stacks")

    if prune:
        logging.info(color("Pruning images..."))
        os.system(f"docker image prune -f")


if __name__ == "__main__":
    update_composes()
