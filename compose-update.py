#!/usr/bin/python3
import os
import click
import tqdm
import multiprocessing as mp

compose_names = {"compose.yaml",
                 "compose.yml",
                 "docker-compose.yaml",
                 "docker-compose.yml"}

def update_compose(x):
    # check if dir exist
    if not os.path.isdir(x):
        raise NotADirectoryError(f"'{x}'")

    # check if dir contains compose file
    compose_file = compose_names.intersection(os.listdir(x))
    if len(compose_file)==0:
        raise FileNotFoundError(f"Directory '{x}' doesn't contain a compose file in one of the following forms: {compose_names}")
    if len(compose_file)>1:
        raise Exception(f"Directory '{x}' contains more then one compose file, namely: {compose_file}")

    # update images
    compose_file = compose_file.pop()
    if os.system(f'docker-compose -f {os.path.join(x, compose_file)} pull') == -1:
        return -1
    if os.system(f'docker-compose -f {os.path.join(x, compose_file)} up -d') == -1:
        return -1
    return 0


@click.command()
@click.argument('update_dirs', nargs=-1)
def update_composes(update_dirs):
    """
    Update docker-compose images automaticly. 
    
    Takes one or more directorys as input and searches for a compose file in one of the following forms:
    "compose.yaml",
    "compose.yml",
    "docker-compose.yaml",
    "docker-compose.yml"

    After the images are updated you will be asked if you want to prune your images.
    """
    update_dirs_set = set(update_dirs)
    pool = mp.Pool(mp.cpu_count())
    
    results = pool.map(update_compose, update_dirs_set)
    pool.close()

    print("\nPrune Images?")
    os.system("docker image prune")

if __name__ == "__main__":
    update_composes()
